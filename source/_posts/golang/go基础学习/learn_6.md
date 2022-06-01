---
title: Go基础学习_5
tags:
- golang
- golang基础学习
---

## 接口

接口可以看成是一种抽象类型，用于告诉"能做什么"的问题。

### 接口定义
```go
type nameer interface {
	方法名1(参数列表1) 返回值列表1
}
一般接口类型后面会带er，比如writer, closer。
当方法名和接口名首字母都是大写的时候，这个方法可以被接口所在之外的代码访问。
```

### 实现接口的条件
接口本质上就是规定了**需要实现的方法列表**，若一个类型实现了接口中规定的所有方法，我们就称它实现了这个接口。

```go
type writer interface {
	write()
}
type P struct {

}
func (p P) write {
	fmt.Println("")
}
```

接口其实和c++中的多态有点相似，一个接口，多种方法，当我们遇到这样的需求的时候，可以使用接口实现，减少代码冗余。

```go
所有类型都有一个say的方法。这样我们可以定义一个对应的接口
type Sayer interface {
	Say()
}
func MakeHungry(s Sayer) {
	s.Say()
}
type Cat struct{}

func (c Cat) Say() {
	fmt.Println("喵喵喵~")
}

type Dog struct{}

func (d Dog) Say() {
	fmt.Println("汪汪汪~")
}

实现了接口类型的变量后，一个接口类型变量能存储所有实现该接口的类型变量
var x Sayer 
a := Cat{}
b := Dog {}
x = a
x.Say()
x = b
x.Say()
```

**值接收者和指针接收者**
对于某个固定的接口，我们使用不同类型实现该接口，使用值接收者实现接口之后，不管是结构体类型还是对应的结构体指针类型的变量都可以赋值给该接口变量。假如使用指针求值，则结构体类型不能直接赋值。

**一个类型可以实现多个接口**
比如对于Sayer和writer可以分开实现且不影响。


**多种类型可以实现同一接口**
比如人可以move, 狗也可以move


接口的所有方法不一定完全由某一类型实现，可以通过在类型中嵌入其他类型或结构体实现。
```go
// WashingMachine 洗衣机
type WashingMachine interface {
	wash()
	dry()
}

// 甩干器
type dryer struct{}

// 实现WashingMachine接口的dry()方法
func (d dryer) dry() {
	fmt.Println("甩一甩")
}

// 海尔洗衣机
type haier struct {
	dryer //嵌入甩干器
}

// 实现WashingMachine接口的wash()方法
func (h haier) wash() {
	fmt.Println("洗刷刷")
}
```

### 接口组合
接口与接口之间可以通过互相嵌套形成新的接口类型，例如go标准库io源码中就有很多接口之间互相组合的例子。

```go
type Reader interface {
	Read(p []byte) (n int, err error)
}

type Writer interface {
	Write(p []byte) (n int, err error)
}

type Closer interface {
	Close() error
}

// ReadWriter 是组合Reader接口和Writer接口形成的新接口类型
type ReadWriter interface {
	Reader
	Writer
}

// ReadCloser 是组合Reader接口和Closer接口形成的新接口类型
type ReadCloser interface {
	Reader
	Closer
}

// WriteCloser 是组合Writer接口和Closer接口形成的新接口类型
type WriteCloser interface {
	Writer
	Closer
}
```

对于多种接口组合形成的新接口类型，同样只需要实现新接口类型中规定的所有方法就算实现了该接口类型。

### 空接口
**空接口可以用于实现泛型**

空接口指没有定义任何方法的接口类型，所以任何类型都可以视为实现了空接口，因此，空接口类型的变量可以用于存储任意类型。

```go
//可以接收任意类型的函数参数
func show(a interface{}) {

}

//作为map的值，存储任意值的字典。
var x = make(map[string]interface{})
```

### 接口值
我们把接口类型看成是抽象类型，接口值实际上是由两个部分组成，实现该接口的类型和值。

**我们不能对空接口值调用任何方法，否则会产生panic**

我们要注意，接口值进行比较的时候必须满足接口的动态类型和动态值都相等的时候才相等。

```go
x Mover = new(Dog)
y Mover = new(Car)
//x != y

同时，若接口值的动态类型相同，但不支持比较，比较的时候会引发panic。
```

### 类型断言
```go
我们可以借助标准库fmt包的格式化打印获取到接口值的动态类型。
var x Mover
m = &Dog{Name: "旺财"}
fmt.Printf("%T\n", m)

go支持类型断言
v, ok = name.(T) //ok表示是否为对应的值
if ok {

} else {

}

可以通过switch语句判断一个接口值的多个类型。

// justifyType 对传入的空接口类型变量x进行类型断言
func justifyType(x interface{}) {
	switch v := x.(type) {
	case string:
		fmt.Printf("x is a string，value is %v\n", v)
	case int:
		fmt.Printf("x is a int is %v\n", v)
	case bool:
		fmt.Printf("x is a bool is %v\n", v)
	default:
		fmt.Println("unsupport type！")
	}
}
```

**接口总的来说是一种抽象类型，可以看成是多态的一种实现方法，能帮我们隐藏某个功能的具体实现，但是我们不能盲目使用接口，不要为了使用接口类型而增加不必要的抽象，只有当多个具体类型以相同方式进行处理时才需要定义接口。**