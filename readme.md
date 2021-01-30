# tips说明

#### 安装
```
wpm install tips
```


#### 使用说明
![tip](https://raw.githubusercontent.com/ev01ing/Wox.Plugin.Tips/master/docs/pics/wox.gif)



#### python依赖

插件使用了time, json, clipboard包，使用前请安装依赖包


#### 中文无法使用的解决办法

这个问题python3下已经解决了，python2还会出现，需要使用下述步骤更正。

1. 找到系统的默认字符集，一般为gbk
2. 找到wox.py的位置，安装目录下的。 可参考 C:\Users\users\AppData\Local\Wox\app-1.3.524\JsonRPC 
3. 将`class wox`的`__init__`第一行改为
`rpc_request = json.loads(sys.argv[1].decode("gbk").encode("utf-8"))`



change log
---

- 2021.01.30 兼容python2和python3，python2的字符集问题还是要手动进行一些更改