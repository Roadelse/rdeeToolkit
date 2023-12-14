# Preface

+ 通用抽象APIs说明, 部分语言已有实现就不管, 没有的自己实现并说明
+ 树结构组织, 最终api要包含父节点的压缩信息


# Basic

+ Basic下的最终api舍去父节点压缩信息
## variable type

### is_array: 判定变量是否为数组
+ **Format :** `is_array(v)`
##### bash
+ `is_array()`
   + 利用`decalre -p`实现, 如果是array, 就echo 1, return 0, 否则echo 0, return 101
   + (*to-be-dev*) 对于`declare -n A=B`这类暂时无法判定, 实际是, 但是会当成不是, 目前

# Array

## querying
### aq_index: 在数组中查询指定element的index
+ Format: `aq_index(arr:array [, element:scalar|arr])`
+ 获取数组arr中目标元素element的所有index
+ 如果不提供element, 那就是作为bool检测true
***
+ 逻辑分层:
   + **L1** : arr一维数组, element单个元素
   + **L2**: arr多维数组, element多维数组(统计时仍然与形状无关, 视作一维数组), 即检索两个数组元素交集在某个数组中的index
#### Python
+ **L1 & L1 :** `numpy.argwhere`
#### ncl
+ **L1 :**  `ind()`, see [doc](https://www.ncl.ucar.edu/Document/Functions/Built-in/ind.shtml)
#### Fortran
+ **L1 :** `ind()`, 手动实现在*rdee_fortran/rdee_array*里

### aq_hasVal: 在数组中查询指定element是否存在
### aq_hasSeq: 在数组中查询指定sequence是否存在
### aq_countVal: 在数组中统计element的个数
### aq_isin: 在数组中查询指定element是否存在
+ **Format :** `aq_hasVal(arr:array, element:scalar)`
+ **Format :** `aq_isin(element:scalar, arr:array)`
+ **Format :** `aq_countVal(arr:array, element:scalar)`
+ 4个函数均属于**aq_index**的弱化版
   * aq_hasVal不需求全部的index, 只看是否有
   * aq_hasSeq不检索单一元素而是检索数组片段
   * aq_isin是hasVal和hasSeg的参数翻转版本, 且兼容这俩
   * aq_countVal不需要统计index只统计个数
***
+ 逻辑分层
   * **L1 :** arr一维数组, element单个元素
   * **L2 :** arr多维数组
   * **L3 :** element多维数组, 即片段检索
#### Python
+ `in, np.argwhere`
#### ncl
+ `ind`
#### Bash
+ `aq_hasVal()`, 手动实现在[](./bash/)中

### remove-elements

#### remove_val(array, val, [nCount = -1], [rev = False])

按照值删除数组中的目标元素
+ array : 总数组
+ val : 目标数值
+ nCount : 个数
+ rev : 是否从右往左

##### in Fortran
+ `remove_val_*`, 实现多组subroutine以达到重载效果
+ **还没做func的版本**

### add-elements

#### union_arr1d(a1, a2, a3, a4, ...)

拼接多个1维度数组 (md, python里都可以直接做)

##### in Fortran
+ 还是得多函数+接口实现类型重载...



## Time

### rdDateTime
*OOP date&time class*
#### General
`§ properties`
+ year, month, day, hour, minute, second, msecond, usecond
`§ methods`
+ operator(+,-)
+ assignment(=)


#### Python
+ `stdlib: datetime`
+ 但是有些缺失的功能需要手动实现/补充
### Direct functions

#### now_str : 获取当前时间的string

`§ in Python`
可以用` time.strftime`实现
`§ in Fortran`
实现了一个`now_str`的函数

#### now : 获取当前时间的ymdhms

`§ in Python`
还是可以用`strftime`或者是`time.localtime()`来搞
`§ in Fortran`
实现了一个`now(year, month, day, hour, minute, second)`的subroutine, 其实就是封装了`date_and_time`啦

#### isLeap : 判断是否是闰年

`§ in Python`
直接`calendar.isleap`
`§ in Fortran`
在`rdee_fortran`里实现了一个`function isLeap(year)`

#### rdTimer(flag, init) : 计时器

标记两次运行之间的耗时, 以flag区分, 以init手动重置, 一般就带个flag就好

`§ in Python`
实现了一个`rdee.rdTimer`
`§ in Fortran`
在rdee_fortran里实现了一个`rdTimer`





