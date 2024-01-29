# README

## 需要的一些依赖

安装`lxml`

```bash
pip install lxml
```

安装`requests`

```bash
pip install requests
```

安装`DrissionPage`

```bash
pip install DrissionPage
```

DrissionPage相关文档地址：[点击这里](https://g1879.gitee.io/drissionpagedocs/get_start/installation)

[🌏 安装 | DrissionPage](https://g1879.gitee.io/drissionpagedocs/get_start/installation)

## 如何调用

**使用例：**

```python
pin=PinterestImageSet()
pin.search('Sousou no frieren')
pin.download(r'C://sousou/')
```

**参数解析**

- `search(self, key, slide=0, random=False)`

该方法用于搜索图片生成结果

`key` 指的是关键词，`slide` 为下拉到底部的次数，默认为0,  `random`是随机参数，问询是否访问首页的推荐图片，默认为`False`

- `download(self, targetUrl='./')`

该方法用于下载图片集合到目的目录

`target` 指的是下载的目的地址，默认为本项目的根目录。
