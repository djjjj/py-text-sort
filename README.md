# PyTextSort

对文本文件进行排序或合并，排序或合并的keys和方法可自定义。


# Quick start

## 安装
> pip install git+

## 使用

### sort
``` 
in_file:
{'id': 'a', 'xxx': 'xxx'}\n
{'id': 'c', 'xxx': 'xxx'}\n
{'id': 'b', 'xxx': 'xxx'}\n
......
``` 
> from PyTextSort import sort_json_file
> sort_json_file(in_file, out_file, ['id'])
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
> from PyTextSort import sort_json_file
> sort_json_file(in_file, out_file, ['id'])
```
out_file:
{'id': 'a', 'x3': 'xxx'}\n
{'id': 'c', 'x1': 'xxx', 'x2': 'xxx'}\n
......
```

