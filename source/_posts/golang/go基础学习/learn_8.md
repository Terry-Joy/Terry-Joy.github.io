---
title: Go基础学习_7
tags:
- golang
- golang基础学习
---

## go语言并发

### Goroutine

Goroutine是Go程序中最基本的并发执行单元。每一个Go程序至少包含了一个main goroutine。Goroutine 是 Go 语言支持并发的核心，在一个Go程序中同时创建成百上千个goroutine是非常普遍的，一个goroutine会以一个很小的栈开始其生命周期，一般只需要2KB。区别于操作系统线程由系统内核进行调度， goroutine 是由Go运行时（runtime）负责调度。

#### go关键字
使用goroutine很简单，在对应的函数和方法前面加上go关键字就可以创建一个goroutine了
```go
go f()

go func() {

}()匿名函数调用

```

假如在main goroutine创建了一个默认的goroutine, 那么当main goroutine结束后，所有由 main goroutine 创建的 goroutine 也会一同退出。

示例
```go
package main

import {
	"fmt"
}

func hello() {
	fmt.Println("hello")
}

func main() {
	go hello()
	fmt.Println("papa")
}
```
我们发现hello语句并没有被打印出来，这是由于main goroutine执行完结束后，剩余的子Goroutine会退出。

### sync包的WaitGroup
当你并不关心并发操作的结果或者有其它方式收集并发操作的结果时，WaitGroup是实现等待一组并发操作完成的好方法。
```go
package main

import (
	"fmt"
	"sync"
)

var wg sync.WaitGroup

func hello() {
	fmt.Println("hello")
	wg.Done() //告知当前goroutine完成
}

func main() {
	wg.Add(1) //登记1个goroutine
	go hello()
	fmt.Println("hello")
	wg.Wait() //阻塞等待登记的goroutine完成	
}
```
可以利用这个同时启动多个Goroutine, 但是要注意这多个Goroutine之间无法确定启动顺序
```go
package main

import (
	"fmt"
	"sync"
)

var wg sync.WaitGroup

func hello() {
	defer wg.Done() //告知当前goroutine完成
	fmt.Println("hello")
}

func main() {
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go hello(i)
	}
	wg.Wait()
}
```

### 动态栈
Goroutine的初始栈空间很小（2KB）, 而实际上分配的空间是并不确定的，Go的runtime会自动为Goroutine分配合适的栈空间。

### Go scheduler
Go的调度器采用的GPM调度模型

### GOMAXPROCS
go运行时的调度器使用GOMAXPROCS参数来确定需要使用多少个OS线程来执行Go代码，现在默认是全部的CPU逻辑核心数。

## channel
现在很多都使用共享内存进行数据交换，但这种并发模型必须使用互斥量对内存进行加锁，这种做法会造成性能问题。go语言采用的并发模型是CSP, 通过通信共享内存而不是共享内存实现通信。

channel是goroutine之间的连接，使得一个goroutine可以发送特定值到另一个goroutine。
channel遵循先进先出的规则，保证收发数据的顺序。

**channel声明格式如下**
```go
var ch1 chan int   // 声明一个传递整型的通道
var ch2 chan bool  // 声明一个传递布尔型的通道
var ch3 chan []int // 声明一个传递int切片的通道
```

**channel零值**
未初始化的通道类型变量其默认零值是$nil$
```go
var ch chan int   
fmt.Println(ch)

//初始化
ch4 := make(chan int, 1)

channel有发送、接收、关闭三种操作，发送和接收都使用<-
初始化
ch := make(chan int)
发送
ch <- 10
接收
x := <- ch
<- ch //从ch中接收值，忽略结果
关闭
close(ch)
```

注意：一个通道值是可以被垃圾回收掉的。通道通常由发送方执行关闭操作，并且只有在接收方明确等待通道关闭的信号时才需要执行关闭操作。它和关闭文件不一样，通常在结束操作之后关闭文件是必须要做的，但关闭通道不是必须的。

关闭后的通道有以下特点：

+ 对一个关闭的通道再发送值就会导致 panic。
+ 对一个关闭的通道进行接收会一直获取值直到通道为空。
+ 对一个关闭的并且没有值的通道执行接收操作会得到对应类型的零值。
+ 关闭一个已经关闭的通道会导致 panic。

### 无缓冲通道
无缓冲通道又被称为阻塞通道。
```go
func main() {
	ch := make(chan int)
	ch <- 10
	fmt.Println("发送成功")
}
```
执行该程序发现goroutine挂起死锁了，出现了deadlock错误。
问题在于无缓冲管道至少需要有一个接收方存在，否则会处于