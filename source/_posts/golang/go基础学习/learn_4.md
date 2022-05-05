---
title: Go基础学习_ 4
tags:
- golang
- golang基础学习
---

## 指针
go里面的指针和c差别在于他是安全指针，无法进行偏移和运算，其他差不多。

里面的指针类型是形如*int这种的。

注意在使用一个指针指向的值时候应该先初始化指针指向的空间

var a* int

```go
new和make都可以用于分配内存
func new(Type) *Type

make区别于new的地方在于slice, map以及chan的内存创建
```

## 类型别名和自定义类型
type TypeAlias = Type

这是一种定义新类型的方法，具有int对应的特性。
type MyInt int 


## 结构体
```go
type person struct {
	name string
	city string
	age int8
}

实例化
var person x1
x1.name = xx

匿名结构体
var user struct {Name string; Age int}
user.Name = ""
user.Age = 18

使用new对结构体实例化
var p2 = new(person)
注意对于指针和对象，都是直接用.来修改和使用成员
p2.name = xx

通过&对结构体取地址相当于对该结构体类型进行了一次new实例操作
p3 := &person{}
p3.name = ""
p3.age = xx
```
### 结构体初始化
未初始化的结构体，成员变量都是对应其类型的零值。
```go
使用键值对初始化

p5 := person{
	name: "小王子",
	city: "北京",
	age:  18,
}
fmt.Printf("p5=%#v\n", p5)

结构体指针也可以进行键值对初始化
p6 := &person{
	name: "小王子",
	city: "北京",
	age:  18,
}
fmt.Printf("p6=%#v\n", p6)
不写初始值默认是该字段的零值

使用值的列表初始化
p8 := &person{
	"沙河娜扎",
	"北京",
	28,
}
注意这种方式
1. 必须初始化结构体的所有字段。
2. 初始值的填充顺序必须与字段在结构体中的声明顺序一致。
3. 该方式不能和键值初始化方式混用。
```

<br>
<br/>
结构体的内存布局

**空结构体不占用内存**

```go
自定义构造函数
func newStudent(name string, age int) *student {
	return &student{name: name, age: age}
}

func main() {
	f1 := newStudent("人", 90)
	fmt.Println(f1)
}
```

### 方法和接收者
接收者可以看成是cpp中this对象，即确定对应的调用对象。

+ 指针类型，会实际修改对应的值
```go
func (name * type) functionName(params ...) {

}

若使用值类型，则无法修改对应的值
func (name type) functionName(params ...) {

}
```

一般使用指针类型的接收者，主要是需要修改接收者的值，拷贝的为较大的对象

**实际上go中可以为任意类型添加方法**。
```go
type MyInt int
func (m MyInt) SayHello() {
	
}
var xx MyInt    
xx.SayHello()
```
**非本地类型不能定义方法，所以我们不能给别的包的类型定义方法。**

### 嵌套结构体
```go
type XX struct {
	Name string
}
type YY struct {
	a XX
}

注意如果在结构体内部没有声明变量的名字，可以看成是以类型名作为变量名。
```

### 结构体字段的可见性
大写字母表示可公开访问，小写表示私有

### 结构体与json序列化
我们可以将结构体转为json字符串，也可以将json字符串转为结构体。
```go
data, err := json.Marshal(c)
err := json.Unmarshal([]byte(str), c1)
```

**注意对于传参是slice, map时，是引用类型，传参的时候需要注意修改问题。**





