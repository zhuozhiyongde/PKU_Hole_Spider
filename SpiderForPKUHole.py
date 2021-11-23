# -*- encoding:utf-8 -*-
#@Time		:	2021/11/23 22:21:52
#@File		:	SpiderForPKUHole.py
#@Author	:	Arthals
#@Contact	:	zhuozhiyongde@126.com
#@Software	:	Visual Studio Code

from selenium import webdriver
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
import selenium
import time
import os
import os.path
import re

# 需安装selenium库4.0.0以上版本
# 需配置webdriver(chromedriver)文件，可自行按照chrome版本下载之后拖入/usr/local/bin
# 终端输入pip3 install selenium或者升级:pip3 install selenium --upgrade

numLog = str(input("是否获取每条信息的编号？获取请输入y，不获取则任意输入非y内容："))
nameLog = str(input("是否获取每条信息的发帖人代称？不获取请输入n，获取则任意输入非n内容："))
collectBool = str(input("是否为获取收藏夹内容？获取请输入y，不获取则任意输入非y内容："))
google = webdriver.Chrome()
url = "https://pkuhelper.pku.edu.cn/hole/"
google.get(url)
# 伪造人工登陆
# 定位登陆按钮
login1 = google.find_element(By.XPATH, "//*[@id='root']/div[4]/div[2]/div/p")
login1.click()
# 定位token输入框
login2 = google.find_element(
    By.XPATH, "//*[@id='pkuhelper_login_popup_anchor']/div/div[2]/p[6]/input")
# 此处填入从设置处获取的登陆Token
login2.send_keys("********************************")
# 定位登陆按钮
login3 = google.find_element(
    By.XPATH, "//*[@id='pkuhelper_login_popup_anchor']/div/div[2]/p[6]/button")
login3.click()
time.sleep(5)

# 判断是否为获取收藏夹
if collectBool == "y":
    login4 = google.find_element(
        By.XPATH, "//*[@id='root']/div[3]/div[2]/div[2]/a[2]/span[1]")
    login4.click()

time.sleep(2)

# 开始不断下拉，直到达到限制，利用每次下滑到xmcp就自动刷新的特性
# 不必再增加循环次数，目前已能达到刷取限制(约为3000条树洞)
for i in range(1, 201):
    try:
        # 定位xmcp，拉入视图中，触发刷新
        target = google.find_element(By.XPATH,
                                     "//*[@id='root']/div[4]/div[2]/p")
        google.execute_script("arguments[0].scrollIntoView();", target)
        try:
            # 点击可能出现的重新加载
            reload = google.find_element(
                By.XPATH, "//*[@id='root']/div[4]/div[2]/div[2]/div/p[1]/a")
            reload.click()
            print("遇到重新加载，请检查网络连接，目前程序仍在继续")
        except:
            # 记录刷取进度
            if i % 20 == 0:
                print("刷取进度：", i / 2, "% \t",
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(2)
    except:
        print("Error:", i)
        continue

# 开始录入
box_content = google.find_elements(By.CLASS_NAME, "box-content")
box_header = google.find_elements(By.CLASS_NAME, "box-header")
# 此处填入目标txt文件地址,Ex."/Users/zhuozhiyongde/Desktop/Essay.txt"
log = open("/Users/zhuozhiyongde/Desktop/Essay.txt", "w+", encoding="UTF-8")
sum = 0
for option in range(len(box_content)):
    header = box_header[option].get_attribute('textContent')
    #匹配树洞编号
    num = re.search("#2\d+", header)
    if num:
        # 判断是否需要抓取树洞编号
        if numLog == "y":
            serial = num.group()
            log.write("--------\n" + serial + "\n")
        # 不抓取的时，仅录入分隔符
        # 某些远古洞可能误判为包含原始树洞号，被误加分隔符，但整体错误率较低
        else:
            log.write("--------\n")
    # 判断是否需要删去代称
    if nameLog == "n":
        text = box_content[option].get_attribute('textContent')

        # 匹配第一个代称
        nameRe = re.match("\[\S+\] ", text)
        if nameRe:
            text = text.lstrip(nameRe.group())
        # 匹配Re代称
        reRe = re.match("Re \S+ ", text)
        if reRe:
            text = text.lstrip(reRe.group())
    else:
        text = box_content[option].get_attribute('textContent')
    log.write(text + "\n")
    sum = sum + 1
    # 打印录入条目，每一百条打印一次
    if sum % 100 == 0:
        print("当前已录入：", sum, "条\t进度：",
              "%.2f" % (sum / (len(box_content)) * 100), "%")
print("总计录入：", sum, "条")
# 退出程序
log.close()
google.quit()