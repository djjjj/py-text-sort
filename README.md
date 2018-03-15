# PyTextSort

对文本文件进行排序或合并，排序或合并的keys和方法可自定义。


# Quick start

## 安装
> pip install git+

# 使用

## 基本

### sort
``` 
in_file:
{'id': 'a', 'xxx': 'xxx'}\n
{'id': 'c', 'xxx': 'xxx'}\n
{'id': 'b', 'xxx': 'xxx'}\n
......
``` 
- from PyTextSort import sort_json_file
- sort_json_file(in_file, out_file, ['id'])
```
out_file:
{'id': 'a', 'xxx': 'xxx'}\n
{'id': 'b', 'xxx': 'xxx'}\n
{'id': 'c', 'xxx': 'xxx'}\n
......
``` 

### merge
``` 
in_file:
{'id': 'a', 'x3': 'xxx'}\n
{'id': 'c', 'x2': 'xxx'}\n
{'id': 'c', 'x1': 'xxx'}\n
......
```
- from PyTextSort import sort_json_file
- sort_json_file(in_file, out_file, ['id'])
```
out_file:
{'id': 'a', 'x3': 'xxx'}\n
{'id': 'c', 'x1': 'xxx', 'x2': 'xxx'}\n
......
```

## 进阶

### 调整参数
PyTextSort入口有三个函数：sort_json_file, sort_json_file, sort_file。每个函数都可以根据实际情况（CPU数量，内存空间，待处理文件大小等），通过调整函数的**block_size**,**p_num**参数来提高程序效率。**block_size**参数指定了输入文件将被切割成多大进行处理，由于文件块是在内存中处理的，所以如果文件块越大，理论上程序处理速度越快，但有内存耗尽的风险；**p_num**参数指定了程序将开辟的进程数，默认值是**CPU核心数+1**，可根据实际情况调节，理论上如果机器的CPU占用率已经到达100%，那么增大**p_num**的数值只会降低程序运行的效率。

