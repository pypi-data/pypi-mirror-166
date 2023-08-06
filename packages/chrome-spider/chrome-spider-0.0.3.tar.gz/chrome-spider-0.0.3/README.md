# chrome-spider

only for mac 

## 1. 安装

```bash
pip3 install chrome-spider
```


## 2. 基本的使用

基于 selenium 封装了一些常用的配置,快速启动

```python
from chrome_spider import Spider

spider = Spider()
driver = spider.get_driver()
driver.get("https://baidu.com")
```
