# FindLinks

Author：木禾

自己用python2写的一个爬页面工具，效果还不错。

## 功能：

1、通过a、frame标签，爬取页面链接。

2、可以设置爬取的级别。

3、具有去重功能。（你也可以在代码里去掉）

## 代码：

```bash
findlinks
│  1.bat # 打开cmd
│  batch.py # 批量：批量域名爬取起始文件
│  findlinks.py # 核心脚本，单域名爬取
│  findlinks.pyc
│  LICENSE
│  README.md
│  urls.txt # 批量：将被爬的的地址
│  urls_old.txt # 批量：已爬的的地址
│
└─Results # 存放爬取结果
```

## 运行：

### 单域名：

`python findlinks.py http://localhost/`

### 批量：

先把域名写入在urls.txt中，然后执行：

`python batch.py`



