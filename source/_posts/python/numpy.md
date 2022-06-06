# 浅谈numpy的使用方法
numpy是一个非常强大的python库，机器学习、图像处理和cv都经常用到，主要在于其对多维数组的支持。

大概十年没写python，这里复习一些简单操作

## python字符串相关
```python
hello = 'hello'    # String literals can use single quotes
world = "world"    # or double quotes; it does not matter.
print(hello)       # Prints "hello"
print(len(hello))  # String length; prints "5"
hw = hello + ' ' + world  # String concatenation
print(hw)  # prints "hello world"
hw12 = '%s %s %d' % (hello, world, 12)  # sprintf style string formatting
print(hw12)  # prints "hello world 12"
```

格式化相关的时候是
```python
'%s' % (xx)
```

相关函数
```python
s = "hello"
print(s.capitalize())  # Capitalize a string; prints "Hello"
print(s.upper())       # Convert a string to uppercase; prints "HELLO"
print(s.rjust(7))      # Right-justify a string, padding with spaces; prints "  hello"
print(s.center(7))     # Center a string, padding with spaces; prints " hello "
print(s.replace('l', '(ell)'))  # Replace all instances of one substring with another;
                                # prints "he(ell)(ell)o"
print('  world '.strip())  # Strip leading and trailing whitespace; prints "world"

str.strip([chars]);
用于移除开头结尾指定的字符串
默认移除头尾\r, \t, \n和空格等字符

s.replace('old', 'new', num)
从左到右替换num次
```
### list
```python
xs = [3, 1, 2]    # Create a list
print(xs, xs[2])  # Prints "[3, 1, 2] 2"
print(xs[-1])     # Negative indices count from the end of the list; prints "2"
xs[2] = 'foo'     # Lists can contain elements of different types
print(xs)         # Prints "[3, 1, 'foo']"
xs.append('bar')  # Add a new element to the end of the list
print(xs)         # Prints "[3, 1, 'foo', 'bar']"
x = xs.pop()      # Remove and return the last element of the list
print(x, xs)      # Prints "bar [3, 1, 'foo']"
```

**loops**
```python
遍历索引加对应值
for id, x in enumerate(animals):
    print('%d %s' % (id + 1, x))
``` 

### 字典
```python
a = {'xx': 'yy'}
for k in a:
    print(a[k])

for k, v in a.items():
    print('%s %s'%(k, v))

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
even = {x: x ** 2 for x in nums if x % 2 == 0}

```

### 集合
注意这里的集合与cpp不同，集合是无序的，所以访问元素的顺序也是无序的。
```python
a = {'xx', 'yy'}
print('xx' in a)
a.add('ff')
a.remove('xx')

遍历
for id, v in enumerate(a):
    print('%d %s' % (id, v))

sets comprehensions

a = {int(sqrt(x) for x in range(30))}
```

### tuples
元组是（不可变的）有序值列表。 元组在很多方面类似于列表; 其中一个最重要的区别是元组可以用作字典中的键和集合的元素，而列表则不能。 这是一个简单的例子：

```python
d = {(x, x + 1): x for x in range(10)}  # Create a dictionary with tuple keys
t = (5, 6)        # Create a tuple
print(type(t))    # Prints "<class 'tuple'>"
print(d[t])       # Prints "5"
print(d[(1, 2)])  # Prints "1"
```

## 数组基础

numpy数组是值网络，所有值类型相同。

### 创建数组
```python
a = np.array([1, 2, 3, 4, 5])
a = np.zeros((2,2))   # Create an array of all zeros
print(a)              # Prints "[[ 0.  0.]
                      #          [ 0.  0.]]"

b = np.ones((1,2))    # Create an array of all ones
print(b)              # Prints "[[ 1.  1.]]"

c = np.full((2,2), 7)  # Create a constant array
print(c)               # Prints "[[ 7.  7.]
                       #          [ 7.  7.]]"

d = np.eye(2)         # Create a 2x2 identity matrix
print(d)              # Prints "[[ 1.  0.]
                      #          [ 0.  1.]]"

e = np.random.random((2,2))  # Create an array filled with random values
print(e)                     # Might print "[[ 0.91940167  0.08143941]
                             #               [ 0.68744134  0.87236687]]"
np.arrage(start = 0, stop, step = 1, dtype)
np.arrage(5)#[0 1 2 3 4 ]

# 用于生成一维等差数列
np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
```

### 生成多维数组
可以通过arange + reshape创建
```python
a = np.arange(20).reshape(4, 5)
```

也可以通过np.array和np.ones和np.zero创建。

同理，三维数组的生成可以
```python
a = np.arange(27).reshape(3, 3, 3)
```

### 多维数组切片
主要通过逗号分离不同维度
两个冒号主要是用于[start = 0::步长]

```python
print(a[0, 1:4]) # >>>[12 13 14]
print(a[1:4, 0]) # >>>[16 21 26]
print(a[::2,::2]) # >>>[[11 13 15]
                  #     [21 23 25]
                  #     [31 33 35]]
print(a[:, 1]) # >>>[12 17 22 27 32]
```
[![XdMb7t.jpg](https://s1.ax1x.com/2022/06/04/XdMb7t.jpg)](https://imgtu.com/i/XdMb7t)

### 数组属性
```python
a = np.array([[11, 12, 13, 14, 15],
              [16, 17, 18, 19, 20],
              [21, 22, 23, 24, 25],
              [26, 27, 28 ,29, 30],
              [31, 32, 33, 34, 35]])

print(type(a)) # >>><class 'numpy.ndarray'>
print(a.dtype) # >>>int64 元素类型
print(a.size) # >>>25
print(a.shape) # >>>(5, 5) 行列数
print(a.itemsize) # >>>8 每个元素的字节数
print(a.ndim) # >>>2  维度
print(a.nbytes) # >>>200 
```

### 基本操作
```python
a = np.arange(25)
a = a.reshape((5, 5)) #重新分配行列

b = np.array([10, 62, 1, 14, 2, 56, 79, 2, 1, 45,
              4, 92, 5, 55, 63, 43, 35, 6, 53, 24,
              56, 3, 56, 44, 78])
b = b.reshape((5,5))
print(a)
print(b)
print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a ** 2)
print(a < b) 
print(a > b)
print(a.dot(b))

print(a.sum()) #求和
print(a.max()) #最大值
print(a.min()) #最小值
print(a.cumsum()) #构造前缀和数组
```

**若数组类型相同，所有操作都是对应的，否则若只有一维相同，可以直接对该维全部操作**

**np.sum的一些注意事项**

```python
a = [[ 1.  2.  3.  4.  5.]
 [ 6.  7.  8.  9. 10.]
 [11. 12. 13. 14. 15.]
 [16. 17. 18. 19. 20.]]


如果axis为整数，axis的取值不可大于数组/矩阵的维度，且axis的不同取值会产生不同的结果。

np.sum(a,axis = 0)
axis为0是压缩行,即将每一列的元素相加,将矩阵压缩为一行，输出：array([34., 38., 42., 46., 50.])

np.sum(a,axis = 1)
axis为1是压缩列,即将每一行的元素相加,将矩阵压缩为一列，输出：array([15., 40., 65., 90.])

```


## 索引进阶
### 花式索引
```python
a = np.arange(0, 100, 10) # 0起点，99终点，步长为10
indices = [1, 5, -1] #选择索引1，5和最后一个元素
b = a[indices]
print(a) # >>>[ 0 10 20 30 40 50 60 70 80 90]
print(b) # >>>[10 50 90]
```

### 缺省索引
```python
a = np.arange(0, 100, 10)
b = a[a >= 60]
print(b)
```

### where函数
```python
a = np.arange(0, 100, 10)
b = np.where(a < 50) 
c = np.where(a >= 50)[0]
print(b) # >>>(array([0, 1, 2, 3, 4]),)
print(c) # >>>[5 6 7 8 9]
```