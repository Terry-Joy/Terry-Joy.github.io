---
title: Go基础学习_1
tags:
- golang
- golang基础学习
---

### 变量声明
```go
package main

func main() {
	//使用var x type声明并初始化
	//var 用于声明， 也可以函数内短变量声明 :=
	//:=等价于 var x type, x = val
	var s string = "xx"
	//自动推导
	var s = "xx"
	s := "xx"
	name, b, c = 12, "xx", 1.0

	//一般这种写法用于全局变量
	var(
		a type, b type2
	)
}

```
注意在函数内声明的都要被使用，全局则不需要，使用_匿名变量可以接值。

## 常量
```go
const a [type] = xx
const {
	a = xx
	b = yy
}
const i, j = 2, 3

//iota可被编译器修改的常量，一开始是0，每一个新的常量声明使iota增加一次
 const (
	a = iota   //0
	b          //1
	c          //2
	d = "ha"   //独立值，iota += 1
	e          //"ha"   iota += 1
	f = 100    //iota +=1
	g          //100  iota +=1
	h = iota   //7,恢复计数
	i          //8
)
//上述打印0, 1, 2
```

## 数据类型
```go
bool
string
uint8, uint16, uint32, uint64
int8, int16, int32, int64
map[string]string
float32, float64
complex64, complex128
[3]int	//数组
[]int //切片
```

## 字符串
go使用"" 或者 `来创建字符串，前者用来创建可解析的字符串而且支持转义，但不能用来引用多行，反引号用来创建原生的字符串字面值，可以由多行构成，但不能转义。双引号用于创建可解析的字符串，反引号则是原生的字符串，用于书写多行消息，html以及正则。
```go
a := "xx"
a := `
	aabb, 
	cc
`

可以使用+=和 +来连接字符串 
```

## 运算符
基本和c++一致，不讲


## 条件语句
```go
a := 18
if a >= 10 {

} else {

}
注意if里面的bool判断不可以用0, 1值来判断

label:
switch  var1{
	case xx:
		...
	break label
	case yy:
		...
}
注意switch只会跑一个
fallthrough可以强制做下一个语句
switch 中加break 可以break到某个标签

```

同时switch支持多条件匹配
```go
switch {
	case 1, 2, 3, 4
	...
}
```

流程控制
下面这些部分千篇一律，所以只会写与别的语言不一样的地方
```go
if a := 15; a >= 15 {

} else {

}

for i := 1; i < 5; i++ {

}

Go语言中可以使用for range遍历数组、切片、字符串、map 及通道（channel）。 通过for range遍历的返回值有以下规律：

数组、切片、字符串返回索引和值。
map返回键和值。
通道（channel）只返回通道内的值。
```

## 数组
```go
[num]type
var a [3]int{1, 4, 3}
var b = [...]int{1, 2}

for i := 0; i < len(a); i++ {
	fmt.Println(a[i])
}

for _, val := range a {
	fmt.Println(val)
}

// 多维数组
dp := [3][2]string{
	{"ss", "dd"},
	{"aa", "ss"},
	{"s", "d"}.
}

for _, v1 := range dp {
	for _, v2 := range v1 {

	}
}
```

**注意： 多维数组只有第一层可以使用...来让编译器推导数组长度。例如：**

数组是值类型，传参的时候复制整个数组，产生的是副本

数组支持 “==“、”!=” 操作符，因为内存总是被初始化过的。
[n]*T表示指针数组，*[n]T表示数组指针 。

## 切片
切片（Slice）是一个拥有相同类型元素的可变长度的序列。它是基于数组类型做的一层封装。它非常灵活，支持自动扩容。

切片是一个引用类型，它的内部结构包含地址、长度和容量。切片一般用于快速地操作一块数据集合。

```go
var name[]type
var name = []type{}

len(name) cap(name)分别求长度和容量

切片表达式[)
[2:] //[2, n)
[2:3] //[2, 3 - 1]
[:3]
[:]

a := b[1:3:5] [low, high, max]
cap设置为max - low

make([]T, size, cap)//构造结构
```

**切片的本质就是对底层数组的封装，它包含了三个信息：底层数组的指针、切片的长度（len）和切片的容量（cap）。**

**切片之间不能比较，数组可以**
**切片为空的时候，要用len(s) == 0判断，不能用nil判断，因为nil值的切片长度和容量都是0，但是我们不能说长度和容量为0的一定是nil**

```go
var a []int   len = cap = 0, nil
b := []int{}		len = cap = 0, not nil
c := make([]int, 0)	len = cap = 0, not nil
```

切片赋值拷贝后，共用同一个底层数组，对一个切片修改会影响另一个切片的内容。

遍历同数组一样

**切片添加元素**
```go
func main() {
	var s[]int
	s = append(s, 1)
	s = append(s, 1, 2, 3)
	s = append(s, s1[1:2], s2[2:3])

	//零值切片没必要初始化
	var a []int
	a = append(a, 1)

	append()函数将元素追加到切片的最后并返回该切片。切片numSlice的容量按照1，2，4，8，16这样的规则自动进行扩容，每次扩容后都是扩容前的2倍。
}
```

**切片本质上是引用类型，如果直接使用赋值，两者底层地址相同，所以要使用copy**

```go
func main() {
	a := []int{1, 2, 3, 4, 5}
	b := a
	b[0] = 4
	fmt.Println(a)
	fmt.Println(b)

	c := []int{1, 2, 3, 4, 5}
	d := make([]int, 4, 4)
	//使用copy复制副本
	copy(d, c)
	fmt.Println(b)
	fmt.Println(c)
}

```

## 删除元素
从切片中删除元素
```go
func main(){
	//删除索引为2
	a = append(a[:2], a[3:])
}
```

## map
```go
定义
map[key]val
a := make(map[int]int, 8)
var a map[int]int

a := map[int]int{}

遍历的话有两种方式
for k, v := range a {

}

for k := range a {

}

delete(map, key) //删除某个key

//注意 go底层的map是基于hash table的，所以是无序的

元素为map类型的切片
func main() {
	var mapSlice = make([]map[string]string, 3)
	for index, value := range mapSlice {
		fmt.Printf("index:%d value:%v\n", index, value)
	}
	fmt.Println("after init")
	// 对切片中的map元素进行初始化
	mapSlice[0] = make(map[string]string, 10)
	mapSlice[0]["name"] = "小王子"
	mapSlice[0]["password"] = "123456"
	mapSlice[0]["address"] = "沙河"
	for index, value := range mapSlice {
		fmt.Printf("index:%d value:%v\n", index, value)
	}
}

值为切片类型的map
var slicemap = make(map[string][]string, 3)
v, ok := slicemap[key]
if !ok {
	v = make([]string, 0, 2)
}

```