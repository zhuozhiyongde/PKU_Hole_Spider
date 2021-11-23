![header.png](https://i.loli.net/2021/11/23/cJSdpBsxDMeUvHq.png)
# PKU_Hole_Spider
## 原文地址
http://www.arthals.ink/?p=62

## 前因
事情的起因是这样的，思修课程写论文，有个可选题目为网络行为规范，我也就因而想整点花活，试着用自己粗浅的Python技术，爬取北大树洞（https://pkuhelper.pku.edu.cn/hole/) 上的内容，并调用百度NLP情绪分析API对样本进行分析。
然而，因为我的技术实在只能算个菜鸟，所以也算是半摸索半做，终于花了两三天才完成了。
以下记录详细的实现过程。

## 爬虫部分
考虑到整个流程需要登陆、下拉等操作，再加上熟悉度的缘故，我选择了使用Selenium库来进行操作，敲了几次初版后，我居然发现这玩意更新到4.0.0版本了：
> zhuozhiyongde@shengxiayuyanhua ~ % pip3 show selenium
> Name: selenium
> Version: 4.0.0
> Summary: None
> Home-page: https://www.selenium.dev
相较于3.0版本，4.0版本提供了更多的操作，并且将以往的`find_element(s)_by_xxx(str)`的定位方法整合到了新的函数`find_element(s)(By.xxx,str)`，显得更加简洁了。

而在实现过程中，最难的无非是确定各种定位方法，以及通过正则表达式匹配一些自己想要的东西，在翻阅了CSDN、Stackoverflow、Runoob等网站之后，也算是渐渐摸索出来了：
### 正则表达式
`re.match("regExp",str)`：从头开始匹配，返回定位元组；

`re.search("regExp",str)`：搜索整个字符串，返回第一个定位元组；

`re.sub("regExp",repl,str,count)`：替换count次匹配到的字符为repl（可以为字符串或是基于匹配到的元组的函数）；

`re.compile("regExp").findall(str,startPos,endPos)`：返回匹配到的元素列表，默认直接group()，如果不group参见返回跌倒器的finditer；

`re.split("regExp",str,maxsplit)`：分割；

`\s`：匹配任意空白字符

`\S`：匹配非空字符

`\d`：匹配数字字符

`\D`：匹配非数字字符

`\b`：匹配单词边界

`\B`：匹配非单词边界

`|`：或

`.`：任意字符

`[...]`：匹配[]内任意字符

`[^...]`匹配任意非[]内字符

`^/$`：开头/结尾

`re+`：匹配≥1个表达式

`re*`：匹配≥0个表达式

`re?`：匹配0个或1个由re定义的片段

`re{n}`：匹配n个表达式

`re{n,}`：匹配≥n个表达式

`re{n,m}`：匹配n~m次个表达式

`()`：分组，记住匹配文本

### Chromedriver
`get_attribute(str)`：获取str标签的内容，可以是src/textContent等，可以通过开发者工具拷贝完整html获知
`find_elements()`：返回一个列表

以上就是所有我新学/复习到的语法，在经过几天更新语法啊、定位方式啊、下拉方式啊、美化代码啊之类的折腾，我终于写出了算是比较完美的爬虫代码：
* 支持选择是否获取主树洞编号（对于某些远古洞可能存在误判）
* 支持选择是否保存代称（对于某些引用洞可能会删除代称失效）
* 支持选择获取收藏夹
* 操作限制，每条树洞最多获取10条以内的回复，超过十条的你直接复制全文吧（doge

完整的爬虫代码参见`main/SpiderForPKUHole.py`：
再次提醒几点使用须知：
* 需安装Selenium 4.0.0以上
* 需装好了Chromedriver
* 需填好了登陆token
* 请勿高强度爬取树洞，增添服务器压力
* 请勿对外扩散此代码
* 更多问题可联系我的邮箱zhuozhiyongde@126.com
