---
title: Go基础学习_2
tags:
- golang
- golang基础学习
---


## fmt库
今天主要讲讲go的fmt标准库

fmt主要负责输出与输入,区别在于$Print$函数直接输出内容，$Printf$函数支持格式化输出字符串，$Println$函数会在输出内容的结尾添加一个换行符。

### Print

``` go
fmt.Print("xxx")
fmt.Printf("%v", xxx)
fmt.Println("xx")
```

### Fprint

Fprint系列函数会将内容输出到一个io.Writer接口类型的变量w中，我们通常用这个函数往文件中写入内容。

```go
func Fprint(w io.Writer, a ...interface{}) (n int, err error)
func Fprintf(w io.Writer, format string, a ...interface{}) (n int, err error)
func Fprintln(w io.Writer, a ...interface{}) (n int, err error)

fileObj, err := os.OpenFile("./xx.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
if err != nil {
	fmt.Println("打开文件出错，err:", err)
	return
}
name := "沙河小王子"
// 向打开的文件句柄中写入内容
fmt.Fprintf(fileObj, "往文件中写如信息：%s", name)
```

### Sprint
Sprint系列函数会把传入的数据生成并返回一个字符串。
```go
s1 := fmt.Sprint("摆了")
name := "hha"
age := 17
s2 := fmt.Sprintf("%s %s", name, age)
```

### Errorf
Errorf函数根据format参数生成格式化字符串并返回一个包含该字符串的错误。
```go
func Errorf(format string, a ...interface{}) error
```

## 格式化占位符
+ 通用占位符
%v		值的默认格式表示
%+v		类似%v，但输出结构体时会添加字段名
%#v		值的Go语法表示
%T		打印值的类型
%%		百分号
<br/>
+ bool型占位符
%t	true/false
<br/>
+ 整型（其实和c差不多）
%b	表示为二进制
%c	该值对应的unicode码值
%d	表示为十进制
%o	表示为八进制
%x	表示为十六进制，使用a-f
%X	表示为十六进制，使用A-F
%U	表示为Unicode格式：U+1234，等价于”U+%04X”
%q	该值对应的单引号括起来的go语法字符字面值，必要时会采用安全的转义表示
<br/>
+ 浮点数与复数
%b	无小数部分、二进制指数的科学计数法，如-123456p-78
%e	科学计数法，如-1234.456e+78
%E	科学计数法，如-1234.456E+78
%f	有小数部分但无指数部分，如123.456
%F	等价于%f
%g	根据实际情况采用%e或%f格式（以获得更简洁、准确的输出）
%G	根据实际情况采用%E或%F格式（以获得更简洁、准确的输出）

```go
f := 12.34
fmt.Printf("%b\n", f)
fmt.Printf("%e\n", f)
fmt.Printf("%E\n", f)
fmt.Printf("%f\n", f)
fmt.Printf("%g\n", f)
fmt.Printf("%G\n", f)

f := 12.34
fmt.Printf("%b\n", f)
fmt.Printf("%e\n", f)
fmt.Printf("%E\n", f)
fmt.Printf("%f\n", f)
fmt.Printf("%g\n", f)
fmt.Printf("%G\n", f)

6946802425218990p-49
1.234000e+01
1.234000E+01
12.340000
12.34
12.34
```

## 字符串和[]byte
%s	直接输出字符串或者[]byte
%q	该值对应的双引号括起来的go语法字符串字面值，必要时会采用安全的转义表示
%x	每个字节用两字符十六进制数表示（使用a-f
%X	每个字节用两字符十六进制数表示（使用A-F）

## 指针

%p 0x十六进制下地址

```go
a := 10
fmt.Printf("%p\n", &a)
fmt.Printf("%#p\n", &a)

0xc000094000
c000094000
```

## 宽度标识符
```go
%f	默认宽度，默认精度
%9f	宽度9，默认精度
%.2f	默认宽度，精度2
%9.2f	宽度9，精度2
%9.f	宽度9，精度0

n := 12.34
fmt.Printf("%f\n", n)
fmt.Printf("%9f\n", n)
fmt.Printf("%.2f\n", n)
fmt.Printf("%9.2f\n", n)
fmt.Printf("%9.f\n", n)

12.340000
12.340000
12.34
    12.34
       12
```

## 输入
### fmt.Scan
```go
func Scan(a ...interface{}) (n int, err error)

Scan从标准输入扫描文本，读取由空白符分隔的值保存到传递给本函数的参数中，换行符视为空白符。本函数返回成功扫描的数据个数和遇到的任何错误。如果读取的数据个数比提供的参数少，会返回一个错误报告原因。

fmt.Scan(&a, &b)
```

### fmt.Scanf 
```go
func Scanf(format string, a ...interface{}) (n int, err error)

Scanf从标准输入扫描文本，根据format参数指定的格式去读取由空白符分隔的值保存到传递给本函数的参数中。
本函数返回成功扫描的数据个数和遇到的任何错误。

和c的用法一样
fmt.Scanf("%v %v", &a, &b)
```

### fmt.Scanln
```go
func Scanln(a ...interface{}) (n int, err error)
```
Scanln类似Scan，它在遇到换行时才停止扫描。最后一个数据后面必须有换行或者到达结束位置。本函数返回成功扫描的数据个数和遇到的任何错误。

## bufio.NewReader
有时候我们想完整获取输入的内容，而输入的内容可能包含空格，这种情况下可以使用bufio包来实现。示例代码如下：

```go
func bufioDemo() {
	reader := bufio.NewReader(os.Stdin) // 从标准输入生成读对象
	fmt.Print("请输入内容：")
	text, _ := reader.ReadString('\n') // 读到换行
	text = strings.TrimSpace(text)
	fmt.Printf("%#v\n", text)
}
```
## Fscan系列
这几个函数功能分别类似于fmt.Scan、fmt.Scanf、fmt.Scanln三个函数，只不过它们不是从标准输入中读取数据而是从io.Reader中读取数据。
```go
func Fscan(r io.Reader, a ...interface{}) (n int, err error)
func Fscanln(r io.Reader, a ...interface{}) (n int, err error)
func Fscanf(r io.Reader, format string, a ...interface{}) (n int, err error)
```

## Sscan系列
这几个函数功能分别类似于fmt.Scan、fmt.Scanf、fmt.Scanln三个函数，只不过它们不是从标准输入中读取数据而是从指定字符串中读取数
据。
```go
func Sscan(str string, a ...interface{}) (n int, err error)
func Sscanln(str string, a ...interface{}) (n int, err error)
func Sscanf(str string, format string, a ...interface{}) (n int, err error)
```