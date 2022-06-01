---
title: Go基础学习_6
tags:
- golang
- golang基础学习
---

## 反射
反射指程序运行期间对程序本身进行访问、检测和修改的能力。支持反射的语言可以在程序编译期将**变量的反射信息，如字段名称、类型信息、结构体信息**等整合到可执行文件中，并给程序提供接口访问反射信息，这样就可以在程序运行期获取类型的反射信息，并且有能力修改它们。

go使用reflect包访问程序的反射信息。

我们可以使用reflect中的TypeOf和ValueOf来获取任意对象的Value和Type

```go
reflect.TypeOf()可以获取值的类型对象

func F(x interface{}) {
	a := reflect.TypeOf(x)
	fmt.Println("type", a)
}
```
<br/>
### type name和type  kind

反射中其实分为type和kind，kind指底层的类型，在反射中，当需要区分指针、结构体等大品种类型，就会用kind。

```go
func reflectType(x interface{}) {
	t := reflect.TypeOf(x)
	fmt.Printf("type:%v kind:%v\n", t.Name(), t.Kind())
}

func main() {
	var a *float32 // 指针
	var b myInt    // 自定义类型
	var c rune     // 类型别名
	reflectType(a) // type: kind:ptr
	reflectType(b) // type:myInt kind:int64
	reflectType(c) // type:int32 kind:int32

	type person struct {
		name string
		age  int
	}
	type book struct{ title string }
	var d = person{
		name: "沙河小王子",
		age:  18,
	}
	var e = book{title: "《跟小王子学Go语言》"}
	reflectType(d) // type:person kind:struct
	reflectType(e) // type:book kind:struct
}
```

**对于go的反射来说，数组、切片、map和指针等类型变量，他们的.name返回空**

下面是reflect包的kind类型
，我们可以发现基本底层类型都覆盖了
```go
type Kind uint
const (
    Invalid Kind = iota  // 非法类型
    Bool                 // 布尔型
    Int                  // 有符号整型
    Int8                 // 有符号8位整型
    Int16                // 有符号16位整型
    Int32                // 有符号32位整型
    Int64                // 有符号64位整型
    Uint                 // 无符号整型
    Uint8                // 无符号8位整型
    Uint16               // 无符号16位整型
    Uint32               // 无符号32位整型
    Uint64               // 无符号64位整型
    Uintptr              // 指针
    Float32              // 单精度浮点数
    Float64              // 双精度浮点数
    Complex64            // 64位复数类型
    Complex128           // 128位复数类型
    Array                // 数组
    Chan                 // 通道
    Func                 // 函数
    Interface            // 接口
    Map                  // 映射
    Ptr                  // 指针
    Slice                // 切片
    String               // 字符串
    Struct               // 结构体
    UnsafePointer        // 底层指针
)
```

### Value of

**reflect.ValeuOf返回的是reflect.Value类型**，包含了原始的值信息，我们可以通过reflect.Value类型提供的获取原始值的方法获取值。

```go
func reflectValue(x interface{}) {
	v := reflect.ValueOf(x)
	k := v.Kind()
	switch k {
	case reflect.Int64:
		// v.Int()从反射中获取整型的原始值，然后通过int64()强制类型转换
		fmt.Printf("type is int64, value is %d\n", int64(v.Int()))
	case reflect.Float32:
		// v.Float()从反射中获取浮点型的原始值，然后通过float32()强制类型转换
		fmt.Printf("type is float32, value is %f\n", float32(v.Float()))
	case reflect.Float64:
		// v.Float()从反射中获取浮点型的原始值，然后通过float64()强制类型转换
		fmt.Printf("type is float64, value is %f\n", float64(v.Float()))
	}
}
func main() {
	var a float32 = 3.14
	var b int64 = 100
	reflectValue(a) // type is float32, value is 3.140000
	reflectValue(b) // type is int64, value is 100
	// 将int类型的原始值转换为reflect.Value类型
	c := reflect.ValueOf(10)
	fmt.Printf("type c :%T\n", c) // type c :reflect.Value
}
```

### 通过反射设置变量的值
想要在函数中通过反射修改变量的值，需要传递变量地址才能修改相应的值，但是我们可以通过reflect的Elem()方法来获取指针对应的值。

```go
package main

import "reflect"

func ref1(x interface{}) {
	a := reflect.ValueOf(x)
	if a.Elem().Kind() == reflect.Int64 {//通过Elem()可以获取指针对应的值
		a.Elem().SetInt(200)
	}
}

func ref2(x interface{}) {
	a := reflect.ValueOf(x)
	if a.Kind() == reflect.Int64 {
		a.SetInt(200)
	}
}

func main() {
	var a int64 = 10
	//ref2(a) 报错，using unaddressable value
	ref1(&a) 
}

```

### isNil()和isValid()
```go
func (v Value) IsNil() bool
```
IsNil()报告v持有的值是否为nil。v持有的值的分类必须是通道、函数、接口、映射、指针、切片之一；否则IsNil函数会导致panic。

```go
func (v Value) IsValid() bool
```
IsValid()返回v是否持有一个值，当v是零值时候返回假，此时除了IsValid(), String, Kind之外的方法都会导致panic

我们一般使用Isnil()来判断指针是否为空，IsValid()用于判定返回值是否有效
```go
func main() {
	// *int类型空指针
	var a *int
	fmt.Println("var a *int IsNil:", reflect.ValueOf(a).IsNil())
	// nil值
	fmt.Println("nil IsValid:", reflect.ValueOf(nil).IsValid())
	// 实例化一个匿名结构体
	b := struct{}{}
	// 尝试从结构体中查找"abc"字段
	fmt.Println("不存在的结构体成员:", reflect.ValueOf(b).FieldByName("abc").IsValid())
	// 尝试从结构体中查找"abc"方法
	fmt.Println("不存在的结构体方法:", reflect.ValueOf(b).MethodByName("abc").IsValid())
	// map
	c := map[string]int{}
	// 尝试从map中查找一个不存在的键
	fmt.Println("map中不存在的键：", reflect.ValueOf(c).MapIndex(reflect.ValueOf("娜扎")).IsValid())
}
```

### 结构体反射
任意值通过$reflect.TypeOf()$获得反射对象的信息后，如果类型是结构体，可以通过reflect.Type的方法获取与结构体成员相关的方法。

```go
Field(i int) StructField	根据索引，返回索引对应的结构体字段的信息。
NumField() int	 		返回结构体成员字段数量。
FieldByName(name string) (StructField, bool)		根据给定字符串返回字符串对应的结构体字段的信息。
FieldByIndex(index []int) StructField	多层成员访问时，根据 []int 	提供的每个结构体的字段索引，返回字段的信息。
FieldByNameFunc(match func(string) bool) (StructField,bool)		根据传入的匹配函数匹配需要的字段。
NumMethod() int					返回该类型的方法集中方法的数目
Method(int) 					Method	返回该类型方法集中的第i个方法
MethodByName(string)(Method, bool)		根据方法名返回该类型方法集中的方法
```

### struct Field类型
StructField类型用来描述结构体中的一个字段的信息。定义如下
```go
type StructField struct {
    // Name是字段的名字。PkgPath是非导出字段的包路径，对导出字段该字段为""。
    // 参见http://golang.org/ref/spec#Uniqueness_of_identifiers
    Name    string
    PkgPath string
    Type      Type      // 字段的类型
    Tag       StructTag // 字段的标签
    Offset    uintptr   // 字段在结构体中的字节偏移量
    Index     []int     // 用于Type.FieldByIndex时的索引切片
    Anonymous bool      // 是否匿名字段
}
```

```go
结构体反射使用示例

package main

import (
	"fmt"
	"reflect"
)

type P struct {
	x int `json: "file"`
	y int `json: "score"`
}

func main() {
	point := P{x: 0, y: 0}
	t := reflect.TypeOf(point)
	fmt.Println(t.Name(), t.Kind())

	for i := 0; i < t.NumField(); i++ {
		f := t.Field(i)
		fmt.Printf("name:%s index:%d type:%v json tag:%v\n", f.Name, f.Index, f.Type, f.Tag.Get("json"))
	}

	if f, ok := t.FieldByName("x"); ok {
		fmt.Printf("name:%s index:%d type:%v json tag:%v\n", f.Name, f.Index, f.Type, f.Tag.Get("json"))
	}
}

```

反射的坏处

+ 基于反射的代码是极其脆弱的，反射中的类型错误会在真正运行的时候才会引发panic，那很可能是在代码写完的很长时间之后。
+ 大量使用反射的代码通常难以理解。
+ 反射的性能低下，基于反射实现的代码通常比正常代码运行速度慢一到两个数量级。