![](https://upload-images.jianshu.io/upload_images/13024789-efcdff6285df1555.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#####  [查看所有Python相关学习笔记](https://www.jianshu.com/p/013cabae8b27)
---
> 此篇文章用于记录学习过程中接触到的与函数有关的知识点
## 函数：
#### 形参：函数创建时括号里的参数
#### 实参：函数调用时括号里的参数(传进来的参数，有具体的值)
#### 函数文档：```函数名.__doc__ # 打印出函数文档 ```
```
def count(info):
    '''
    :param info: 格式：'姓名1,：age1,姓名2:age2，...'
    :type info:str
    :return: (maxNumAge, maxNum)
    :rtype:list
    计算字符串内哪个年龄的人数最多，并返回人数最多的年龄和该年龄的人数
    '''
    pass
a = 'hasen1 :13,tom mark : 33,hasen3:13,hasen4:13,hasen5:33,   hasen5:40'
count(a)

```
- :param a -->指明参数为a
- :type a:int  -->指明参数a的类型为int
- :return:a*2  -->指明返回的内容
- :rtype:int   -->指明返回的类型
- 调用函数时，按住ctrl，鼠标指向调用参数的位置可以查看该函数的参数个数、类型，以及返回类型
```
显示内容如下：
---def count(info)
---inferred type:(info:str) -> list
```
```
>>>print(count.__doc__) #打印查看此函数文档
    :param info: 格式：'姓名1,：age1,姓名2:age2，...'
    :type info:str
    :return: (maxNumAge, maxNum)
    :rtype:list
    计算字符串内哪个年龄的人数最多，并返回人数最多的年龄和该年龄的人数

```



#### 必选参数：避免因顺序问题调用错误(一旦第n个参数使用了关键字传参，后面的都必须使用)
```
def SaySome(name,words):
	print(name+ '-->'+words)
SaySome(name='hasen',words='hello world')

# 执行结果
hasen-->hello world
```
#### 默认参数：为形参定义初值，调用时若忘记传值，则使用初始值
```
def SaySome(name,words='hello world'):
	'某人说...'
	print(name+ '-->'+words)
SaySome(name='hasen0')
SaySome(name='hasen1',words='i love python')

# 执行结果
hasen0-->hello world
hasen1-->i love python
```  
    
#### 可更改与不可更改的参数
> 所有的变量都可以理解是内存中的一个对象的“引用”，而对象有两种，“可更改（mutable）”与“不可更改（immutable）”对象。在python中 ，strings,tuples和numbers是不可更改的对象，而list,dict等则是可以修改的对象

#### 收集参数
> 如果收集参数后面有其他参数，则调用其他参数时要采用关键字参数的调用方法，否则会报错。一般情况下，该其他参数会定义一个默认值（例如print函数中的end等)。  
> *args是可变参数，args接收的是一个tuple：
```
def func(a,b,c=0,*args):
    print(a,b,c,args)
func(1,2,3,*[1,2,3,4])
func(1,2,3,[1,2,3,4])
func(1,2,3,4)
# 执行结果
1 2 3 (1, 2, 3, 4)
1 2 3 ([1, 2, 3, 4],)
1 2 3 (4,)
``` 

```
def test(*params,exp=0):
	'收集参数...'
	print('参数的长度是：',len(params))
	print('exp:',exp)
test(1,2,3,exp = 4)
test(1,2,3,4)
# 执行结果
参数的长度是： 3
exp: 4
参数的长度是： 4
exp: 0
```  
#### 关键字参数
> 关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。  
- **kw是关键字参数，kw接收的是一个dict。  
    
    ```
    def person(name, age, **kw):
        print('name:', name, 'age:', age, 'other:', kw)
        
    person('Adam', 45, gender='M', job='Engineer')
    # 执行结果
    name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
    ```
#### 命名关键字参数  
- 如果要限制关键字参数的名字，就可以用命名关键字参数，例如，只接收city和job作为关键字参数。这种方式定义的函数如下：
```
def person(name, age, *, city, job):
    print(name, age, city, job)
```
- 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数。调用方式如下：
```
>>> person('Jack', 24, city='Beijing', job='Engineer')
Jack 24 Beijing Engineer
```
- 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了：
```
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
```
- 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错：
```
>>> person('Jack', 24, 'Beijing', 'Engineer')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: person() takes 2 positional arguments but 4 were given
```
- 由于调用时缺少参数名city和job，Python解释器把这4个参数均视为位置参数，但person()函数仅接受2个位置参数。

- 命名关键字参数可以有缺省值，从而简化调用：
```
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job)
```
- 由于命名关键字参数city具有默认值，调用时，可不传入city参数：
```
>>> person('Jack', 24, job='Engineer')
Jack 24 Beijing Engineer
```
- 使用命名关键字参数时，要特别注意，如果没有可变参数，就必须加一个*作为特殊分隔符。如果缺少*，Python解释器将无法识别位置参数和命名关键字参数：
```
def person(name, age, city, job):
    # 缺少 *，city和job被视为位置参数
    pass
```

#### 参数组合
> 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。

- 比如定义一个函数，包含上述若干种参数：
```
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)
```
- 在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。
```
>>> f1(1, 2)
a = 1 b = 2 c = 0 args = () kw = {}
>>> f1(1, 2, c=3)
a = 1 b = 2 c = 3 args = () kw = {}
>>> f1(1, 2, 3, 'a', 'b')
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
>>> f1(1, 2, 3, 'a', 'b', x=99)
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}
>>> f2(1, 2, d=99, ext=None)
a = 1 b = 2 c = 0 d = 99 kw = {'ext': None}
```
- 最神奇的是通过一个tuple和dict，你也可以调用上述函数：```dict中的key只能是字符串时才可以```
```
>>> args = (1, 2, 3, 4)
>>> kw = {'d': 99, 'x': '#'}
>>> f1(*args, **kw)
a = 1 b = 2 c = 3 args = (4,) kw = {'d': 99, 'x': '#'}
>>> args = (1, 2, 3)
>>> kw = {'d': 88, 'x': '#'}  # key值必须是字符串
>>> f2(*args, **kw)
a = 1 b = 2 c = 3 d = 88 kw = {'x': '#'}
```
- 所以，对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。  
***注：虽然可以组合多达5种参数，但不要同时使用太多的组合，否则函数接口的可理解性很差。***


#### 返回值:
通过return返回，如果return后无内容或不写return，则函数默认返回None
如果返回多个值，则默认返回一个元组
可以人工定义为一个列表，return意味着函数的结束，函数内return后面即使有千万条代码也不执行

```
def back():
        print(1*2)
print(back)

def back():
	return 1,'a',3.4
print(back())

def back2():
	return [1,'a',3.4]
print(back2())

# 执行结果
2
None
(1, 'a', 3.4)
[1, 'a', 3.4]
```
    
#### 全局变量：定义在模块外的变量  
#### 局部变量：定义在模块内的变量
#### [关键字（global & nonlocal）](https://www.cnblogs.com/z360519549/p/5172020.html)
- 在函数内定义的函数都是局部变量，函数外无法访问;
- 函数内可以访问全局变量，但不要修改全局变量的值;
- 函数中如果试图去修改全局变量，此时函数会自动创建一个新的同名的局部变量，此时修改的其实只是函数内的该局部变量。如果一定要修改，可以在函数内使用global关键字修饰该变量 
- global关键字用来在函数或其他局部作用域中使用全局变量。但是如果不修改全局变量也可以不使用global关键字。
- nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量。
```
count = 5
def MyFun():
	count = 10
	print(count)
MyFun()
print(count)

# 执行结果
10
5
```

```
count = 5
def MyFun():
	global count
	count = 10
	print(count)
MyFun()
print(count)

# 执行结果
10
10
```

#### 内嵌函数：函数内部创建另一个函数，内部的这个函数就是内嵌函数
> 内嵌函数仅在外部函数内的作用域可以调用，在外部函数外无法调用  



```
def fun1():
	print('fun1()正在被调用...')
	def fun2():
		print('fun2()正在被调用...')
	fun2()
fun1() 
# 执行结果
fun1()正在被调用...
fun2()正在被调用...
```
#### [闭包(词法闭包&函数闭包)](https://www.jianshu.com/p/15570ace1af9)
> 引用了自由变量的函数。这个被引用的自由变量将和这个函数一同存在，即使已经离开了创造它的环境也不例外。  
> 在一些语言中，在函数中可以定义另一个函数时，如果内容函数引用了外部的函数的变量，则可能产生闭包。运行时，一旦外部的函数被执行，一个闭包就行程了，闭包中包含了内部函数的代码，以及所需外部函数中的变量的引用。

```
def FunX(x):
	def FunY(y):
		return x * y
	return FunY

i = FunX(8)
print(type(i))
print(i(5))
print(FunX(8)(5))

# 执行结果
<class 'function'>
40
40
```
```
def fun1():
	x = 5
	def Fun2():
		nonlocal x  #python3关键字，不加此行时，调用Fun1时会报错，因为Fun2在修改x的值
		x *= x
		return x
	return Fun2()
print(fun1())

# 执行结果
25
```


#### lambda表达式(匿名函数)
> Python写一些执行脚本时，使用lambda就省下了定义函数的过程，比如说我们只是需要写个简单的脚本来管理服务器时间，我们就不需要专门定义一个函数然后在写调用，使用lambda就可以使得代码更加精简。    
> lambda不用考虑给函数命名的问题    
> 简化代码的可读性 

```
add = lambda x,y:x+y
add(3,4)

# 执行结果
7
```
#### 两个比较牛逼的BIF
- **filter()**```过滤器 filter(function or None, iterable)```
> 1、第一个参数为None时，返回的结果为：iterable中为True的结果  
> 2、第一个参数为一个function时，返回结果为：iterable中过滤掉function的return值的结果

```
# 为None时
g = list(filter(None,[1,0,False,True]))
print(g)

# 执行结果
[1, True]
```
```
# 为function时
def odd(x):
	return x % 2
temp = range(10)
show = filter(odd,temp)
h = list(show)
print(h)

# 执行结果
[1, 3, 5, 7, 9]
```
```
# 结合lambda
j = list(filter(lambda x:x%2,range(10)))
print(j)

# 执行结果
[1, 3, 5, 7, 9]
```
- **map()** ```映射 map(func, *iterables) --> map object```
> 将第二个参数中的元素（序列）传入func中，生成一个新的序列  

```
g = list(map(lambda x:x*2,range(10)))
print(g)

# 执行结果
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

#### 递归函数
> 函数调用自身的行为  
> Python3对递归默认深度的设置是100层  

```
# 手动设置递归深度
import sys
sys.setrecursionlimit(100000)
```
- 汉诺塔游戏
- 树结构的定义
- 歇尔宾斯基三角形
- 女神自拍（递归）
- **例子**：写一个求阶乘的函数
	- 正整数阶乘指从1乘以2乘以3乘以4一直乘到所要求的数
	- 例如所给的数是5，则阶乘式是1 X 2 X 3 X 4 X 5，得到的积是120，所以120就是4的阶乘
```
# 非递归方式实现
def jieC(num):
	total = 1
	for i in range(1,num+1):
		total = total* i
	return total
print(jieC(5))

# 执行结果
120


# 递归方式实现
def diGui(num):
	if num == 1:
		return 1
	else:
		return num * diGui(num-1)
result = diGui(5)
print(result)

# 执行结果
120
```
## 函数调用时加括号和不加括号的区别
- 不带括号时，调用的是这个函数本身 ，是整个函数体，是一个函数对象，不须等该函数执行完成
- 带括号（参数或者无参），调用的是函数的执行结果，须等该函数执行完成的结果
```
def test():
    a = 'hello dddddd'
    return a
print(test)
print(test())

# 执行结果
<function test at 0x101bcbe18>
hello dddddd
```



