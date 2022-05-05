---
title: Go基础学习_3
tags:
- golang
- golang基础学习
---

## function

go语言中支持函数、匿名函数和闭包，且函数在go中属于一等公民

```go
注意函数参数
func sum(x int32, y int32) int32 {
	return x + y
}

函数的参数中如果相邻变量的类型相同，则可以省略类型
func intSum(x, y int) int {
	return x + y
}


可变参数只能放在函数的最后位置
func intSum2(x ...int)int {
	for _, v := range(x) {
		
	}//本质上是通过切片实现的
}
可以传入多个参数

可以使用多返回值
func cal(x, y int) (int, int) {
	return suma, sumb
}

函数定义时可以给返回值命名，并在函数体中直接使用这些变量，最后通过return关键字返回

func calc(x, y int) (sum, sub int) {
	sum = x + y
	sub = x - y
	return
}
```

## 函数进阶
### 变量作用域
和cpp一致，不讲

### 函数类型
```go
type name func(int, int) int

func add(x, y int) int {
	return x + y
}

var x type
x = add
```

```go
func main() {
	var c type
	c = add

	//将函数add赋值给变量
	f := add
	fmt.Println(f(10, 20))
}
```

### 高阶函数
（1）函数可以作为参数
```go
func add(x, y int, op func(int, int) int) int {
	return op(x, y)
}

//传入函数作为参数
a := add(10, 20, cal)
```
（2）函数可以作为返回值
```go
func do(s string) (func(int, int) int, error) {
	switch s {
	case "+":
		return add, nil
	case "-":
		return sub, nil
	default:
		err := errors.New("无法识别的操作符")
		return nil, err
	}
}
```

### 匿名函数
```go
func(参数)(返回值) {

}

// 将匿名函数保存到变量
add := func(x, y int) {
	fmt.Println(x + y)
}
add(10, 20) // 通过变量调用匿名函数

//自执行函数：匿名函数定义完加()直接执行
	func(x, y int) {
		fmt.Println(x + y)
	}(10, 20)
```

**匿名函数多用于实现回调函数和闭包, 可以作为返回值**

Go语言中只存在值传递（要么是该值的副本，要么是指针的副本），不存在引用传递。之所以对于引用类型的传递可以修改原内容数据，是因为在底层默认使用该引用类型的指针进行传递，但是也是使用指针的副本，依旧是值传递。

### 闭包
闭包指的是一个函数和与其相关的引用环境组合而成的实体。简单来说，闭包=函数+引用环境。 

```go
func adder() func(int) int {
	var x int
	return func(y int) int {
		x += y
		return x
	}
}
func main() {
	var f = adder()
	fmt.Println(f(10)) //10
	fmt.Println(f(20)) //30
	fmt.Println(f(30)) //60

	f1 := adder()
	fmt.Println(f1(40)) //40
	fmt.Println(f1(50)) //90
}
我们发现f就是一个闭包，在f的生命周期内，变量x也一直有效。

func calc(base int) (func(int) int, func(int) int) {
	add := func(i int) int {
		base += i
		return base
	}

	sub := func(i int) int {
		base -= i
		return base
	}
	return add, sub
}

func main() {
	f1, f2 := calc(10)
	fmt.Println(f1(1), f2(2)) //11 9
	fmt.Println(f1(3), f2(4)) //12 8
	fmt.Println(f1(5), f2(6)) //13 7
}
在闭包内部，所有的变量会与闭包的生命周期共存.
```

### defer语句
go里面的defer语句会将跟随在其后的语句延迟处理。在$defer$归属的函数即将返回时，再将defer定义的逆序进行，用于资源清理、文件关闭、解锁及记录时间等。

**go的return并非原子操作，分为2部分，给返回值赋值和RET指令两步，defer语句执行的时机就在给返回值复制后。**
可以看成是 返回值 = x, defer, return

注意defer有几个重要特性。
+ defer被声明的时候，参数会被实时解析
```go
func a() {
	i := 0
	defer fmt.Println(i) //此时解析为0
	i++
}
```

+ defer的执行是先进后出
+ defer可以读取有名返回值
```go
func c() (i int) {
	defer func() { i++ }()
	return 1
}
这里输出为2。
```

最后大家可以看一下下面四个的输出，如果能彻底理解了，就问题不大了。
```go
func f1() int {
	x := 5
	defer func() {
		x++
	}()
	return x
}

func f2() (x int) {
	defer func() {
		x++
	}()
	return 5
}

func f3() (y int) {
	x := 5
	defer func() {
		x++
	}()
	return x
}
func f4() (x int) {
	defer func(x int) {
		x++
	}(x)
	return 5
}
func main() {
	fmt.Println(f1())
	fmt.Println(f2())
	fmt.Println(f3())
	fmt.Println(f4())
}
输出是5655
浅析一下
f1:
r := x = 5
x++
return r

f2:
x = 5
x++
return x

f3:
y := x = 5
x++
return y

f4:
外层x = 5
内层refer传参的x副本 = 6
return 外层x
```

```go
再来一个简单的面试题
func calc(index string, a, b int) int {
	ret := a + b
	fmt.Println(index, a, b, ret)
	return ret
}

func main() {
	x := 1
	y := 2
	defer calc("AA", x, calc("A", x, y))
	x = 10
	defer calc("BB", x, calc("B", x, y))
	y = 20
}
```

内置函数介绍
**close**		主要用来关闭channel
**len**			用来求长度，比如string、array、slice、map、channel
**new**			用来分配内存，主要用来分配值类型，比如int、struct。返回的是指针
**make**		用来分配内存，主要用来分配引用类型，比如chan、map、slice
**append**		用来追加元素到数组、slice中
**panic和recover**		用来做错误处理

```go

func funcA() {
	fmt.Println("func A")
}

func funcB() {
	defer func() {
		err := recover()
		//如果程序出出现了panic错误,可以通过recover恢复过来
		if err != nil {
			fmt.Println("recover in B")
		}
	}()
	panic("panic in B")
}

func funcC() {
	fmt.Println("func C")
}
func main() {
	funcA()
	funcB()
	funcC()
}
recover()必须搭配defer使用
defer一定要在可能引发Panic的语句之前定义
```