# coding=utf-8

import os
import time
import json
import html
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 以下为启动Chrome，并打开调试端口、新建配置文件的命令行。按需修改和调用
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Public\ChromeData"


# 打印日志
def log(str=""):
  print("gpttalk: [%s] %s" % (datetime.datetime.now(), str))

class ChatGPT(object):
  GPT_status = 'finish'
  # 初始化，连接开了本地端口调试的Chrome浏览器
  def init(self, port):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:%d" % port)
    log("尝试在端口 %d 上连接浏览器" % port)
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}
  # 关闭
  def close(self):
    self.driver.quit()

  # 打开ChatGPT网页。
  # 参数：
  # 1.delay:等待网页加载的秒数
  # 2.refresh:设为True，则强制Chrome重新载入网页。但会频繁触发CloudFlare。
  #    设为False，则什么都不做。但需要事先将浏览器开好。我是将ChatGPT设成了首页
  def open(self, delay=3, refresh=False):
    log("打开ChatGPT网页中...")
    if refresh:
      self.driver.get("https://chat.openai.com")
    time.sleep(delay)
    log("完成")

  # 向ChatGPT发送文本。delay为每个步骤间延迟的秒数。
  def send(self, msg="你好", delay=0.25):
    # 点击文本框
    txtbox = self.driver.find_element(By.CSS_SELECTOR, ".m-0")
    txtbox.click()
    time.sleep(delay)
    # 输入文本，需处理换行
    txtbox.clear()
    log("发送内容:"+repr(msg))
    txtbox.send_keys(str(msg))
    time.sleep(5)
    # 发送
    txtbox.send_keys(Keys.ENTER)
    time.sleep(2)

  # 重新生成
  def regenerate(self):
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()


  # 判断ChatGPT是否正忙或者出错
  def gptBusyorFree(self):
    with open(".\js\detec_status.js", "r") as js_file:
      script = js_file.read()
      gpt_status = self.driver.execute_script(script)
    log(gpt_status)
    return gpt_status

  # 获取最近一条回复
  def getReplyList(self):
    with open(".\js\getReply.js", "r",encoding='utf-8') as js_file:
      script = js_file.read()
      output = self.driver.execute_script(script)
    output = output.replace("<p>","").replace("</li>","").replace("\n","")
    output = html.unescape(output)
    outputarry = output.split("</p>")
    output = ""
    i = 1
    for text in outputarry:
        if("<li>" in text):
            text = str(i) + ". " + text.replace("<li>","")
            i = i + 1
        output = output +"\n\n"+ text
    return output

  # 等待回复
  def getLastReply(self):
    log("等待回复中...")
    # 判断ChatGPT是否正忙
    GPT_status = self.gptBusyorFree()
    while('working' in GPT_status):
      time.sleep(2)
      GPT_status = self.gptBusyorFree()
      log(GPT_status)
    if('error' in GPT_status):
      return ('🤦‍♀️GPT出现错误，请刷新网页或者查看后台🤦‍♂️')
    else:
      return self.getReplyList()

# if __name__=="__main__":
#   chatgpt = ChatGPT()
#   chatgpt.init(9222)
#   chatgpt.open()
#   log(chatgpt.getReplyList())
#   while True:
#     msg = input("=====================\n请输入内容，Ctrl+Q重开，Ctrl+R重新生成，Ctrl+C退出\n>>> ")
#     if msg.find(chr(17)) > -1:
#       chatgpt.open(refresh=True)
#     elif msg.find(chr(18)) > -1:
#       chatgpt.regenerate()
#     else:
#       chatgpt.send(msg=msg)
#       time.sleep(5)
#       chatgpt.getLastReply()
