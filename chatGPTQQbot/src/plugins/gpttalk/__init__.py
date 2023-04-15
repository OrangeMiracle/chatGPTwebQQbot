from nonebot import on_keyword
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.rule import to_me
import asyncio
from typing import (Any, Callable, Awaitable, Iterable, List)
from quart.utils import run_sync
from js import GPTIO
from revChatGPT.V1 import Chatbot
import time
import re
import sqlite3
import csv
import datetime
import nonebot



# 打印日志
def log(str=""):
  print("gpttalk: [%s] %s" % (datetime.datetime.now(), str))

####################以下代码与需要打开浏览器无关####################
class Gpt_account:
    def __init__(self, bot,email_,status_):
        self.bot = bot
        self.email = email_
        self.status = status_

#active_nobowser=False   #启动不需要打开浏览器的部分
active_bowser=(False or not('false' in str(nonebot.get_driver().config.active_bowser).lower()))     #启动需要打开浏览器的部分,在.env.dev文件中修改，默认为False
conn = sqlite3.connect('./js/qqgroup_userinfo.db')
c = conn.cursor()
# conn.close()
gpt_accounts = []
black_list = []
def get_gpt_accounts():
    return gpt_accounts
def set_gpt_accounts(account_list):
    gpt_accounts = account_list
def get_black_list():
    return black_list
# 读取黑名单
with open("./js/black_list.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            userid = row['blacklist']
            black_list.append(str(userid))
        except Exception:
            log("加载黑名单出现问题")

#  读取GPT access_token信息登录
with open("./js/ghotmail_account.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            plus_status = row['plus_status'].lower()
            token = row['access_token']
            config = {
                "access_token": token,
                "paid": False
                if not ("true" in plus_status)
                else    True,
            }
            chatbot = Chatbot(config=config)
            
            account = Gpt_account(chatbot,str(row['email']),'finish')
            log(row['email'])
            gpt_accounts.append(account)
            log(f"{row['email']} 登陆成功")

        except Exception:
            log(f"token账户登录出现问题:   {row}")

#  读取GPT邮箱账号数据并逐一登录
with open("./js/user_account.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            email = row['email']
            password = row['password']
            plus_status = row['plus_status'].lower()
            config = {
                "email": email,
                "password": password,
                "paid": False
                if not ("true" in plus_status)
                else    True,
            }
            chatbot = Chatbot(config=config)
            account = Gpt_account(chatbot,str(row['email']),'finish')
            log(row['email'])
            gpt_accounts.append(account)
            log(f"{row['email']} 登陆成功")
        except Exception:
            log(f"邮箱账户登录出现问题:   {row}")




#  向GPT提问
@run_sync
def askGPT_nobowser(gptbot,question,convid=None):
    prev_text = ""

    # covid='7ae51b08-a450-437f-ae06-35d903c6616a'
    # allgistory = chatbot.get_msg_history(covid)
    # parid= str(list(allgistory['mapping'].keys())[-1])
    # for data in chatbot.ask(
    #     prompt = "厉害",
    #     conversation_id=covid,
    #     parent_id=parid
    # ):
    #     response = data["message"]
    # log(response)


    if(convid is None):
        for data in gptbot.ask(
            prompt=question,
            conversation_id=convid
        ):
            #print(data)
            message = data["message"][len(prev_text) :]
            #print(message, end="", flush=True)
            prev_text = data["message"]
    else:
        allgistory = gptbot.get_msg_history(convid)
        parid= str(list(allgistory['mapping'].keys())[-1])
        for data in gptbot.ask(
            prompt = question,
            conversation_id  = convid,
            parent_id = parid
        ):
            #print(data)
            #print(message, end="", flush=True)
            prev_text = data["message"]
    return prev_text

# #   等待GPT回复
# async def waitreply_nobowser(gptbot,question,convid=None):
#     result = await askGPT_nobowser(gptbot,question,convid)
#     return result
# #   等待GPT回复之套娃
# def waitreply_nobowser2(gptbot,question,convid=None):
#     result = asyncio.run(waitreply_nobowser(gptbot,question,convid=None))
#     return result


askGPT_nobowser_awake=on_message(rule=to_me(),priority=200)
@askGPT_nobowser_awake.handle()
async def _(event: GroupMessageEvent):
    uid=event.user_id
    #查看是是否在黑名单
    if str(uid) in black_list:
        await word.finish(Message(f"[CQ:at,qq={uid}]你在黑名单中,不可使用"))
    if (len(get_gpt_accounts()) < 1):
        await word.finish(Message(f"[CQ:at,qq={uid}]没有登陆任何GPT账号"))
    #在数据库中寻找提问的人是否存在，如果不存在，则从gpt账号列表中寻找目前空闲的账号，创建这一行
    #这里其实应该用map或者dictionary之类的来定位空闲的gpt账号，但是我还没搞懂python里怎么用这些东西，刚学没多久🤣
    user_msg = event.message
    c.execute("SELECT * FROM userinfo WHERE userid = ?", [str(uid)])
    row = c.fetchone()
    time.sleep(0.5)
    account_list = get_gpt_accounts()
    if row is not None and not('None' in row[3]):
        i = 0
        for x in account_list:
            email = account_list[i].email
            bot = account_list[i].bot
            if((row[2] in email)): #这里需要确认   1.群友上次用的是哪一个账号  
                if(str(row[3]) in str(account_list[i].bot.get_conversations())): #2.它使用的对话是否还存在
                    while('working' in account_list[i].status):
                        time.sleep(0.5)
                        account_list = get_gpt_accounts()
                    
                    account_list[i].status = 'working'
                    set_gpt_accounts(account_list)


                    gpt_result = await askGPT_nobowser(bot, str(user_msg), str(row[3]))


                    c.execute("UPDATE userinfo SET conversationid = ? WHERE userid = ?", (str(row[3]), str(uid)))
                    conn.commit()

                    account_list[i].status = 'finish'
                    set_gpt_accounts(account_list)

                    await word.finish(Message(f"[CQ:at,qq={uid}]GPT {email}:\n{gpt_result}"))
                    break
                else:
                    break
            i = i + 1

    #这里放一个更新点，如果有GPT账户没有被任何人使用，那就给用户分配那个没被使用的账户
    
    #如果数据库记录中有用户使用记录，但是它使用的账号和对话不在这次的所有登陆GPT账号中，则删除所有这个用户在数据库中的数据，并视为新用户
    c.execute("DELETE FROM userinfo WHERE userid = ?", (str(uid),))
    conn.commit()
    log(f'新用户{uid}') 
    
    while(True):
        log('新用户while')
        i = 0
        time.sleep(0.5)
        account_list = get_gpt_accounts()
        for x in account_list:
            time.sleep(0.2)
            if('working' in x.status):  #为啥我要用一个list里面的值表示状态来标记当前任务是否能用呢，因为我还没学会多线程😅
                account_list = get_gpt_accounts()
            else:
                account_list[i].status = 'working'
                set_gpt_accounts(account_list)

                account_list[i].bot.reset_chat()
                bot = account_list[i].bot
                email = account_list[i].email
                groupid = event.group_id
                gpt_result = await  askGPT_nobowser(bot, str(user_msg))#如果不输入对话id，那就是创建新的会话，会话id要问完才会获取
                covid = bot.conversation_id
                bot.change_title(covid,uid)
                log(f'新用户{uid}')
                c.execute("INSERT INTO userinfo (userid, groupid, gptaccount,conversationid) VALUES (?, ?,?,?)", (str(uid),str(groupid),str(email),str(covid)))
                conn.commit()

                account_list = get_gpt_accounts()
                account_list[i].status = 'finish'
                set_gpt_accounts(account_list)
                await word.finish(Message(f"[CQ:at,qq={uid}]GPT {email}:\n{gpt_result}"))               
            account_list = get_gpt_accounts()
            i = i + 1




####################以下所有代码全部是有关需要打开浏览器的部分####################


word=on_keyword({"在吗"},rule=to_me(),block=True,priority=12)
@word.handle()
async def _(event: GroupMessageEvent):
    uid=event.user_id
    msg = "好👌"
    await word.finish(Message(f"[CQ:at,qq={uid}]{msg}"))


if(active_bowser):
    chatgpt = GPTIO.ChatGPT()
    chatgpt.init(9222)
    chatgpt.open()
    #向GPT发送消息
    askGPT_awake=on_keyword({"!web"},rule=to_me(),priority=100)
    @askGPT_awake.handle()
    async def _(event: GroupMessageEvent):
        uid=event.user_id
        #msg = "🙅‍♀️不好🙅‍♂️ "
        if("finish" in chatgpt.gptBusyorFree()):
            user_msg = event.message
            # 下面这行代码，是向gpt发送消息
            # 有时候用户输入文本会遇到一些奇怪的换行格式导致只发送一半的文本
            # 如果使用utf8，encode之后给GPT，他也能读懂(毕竟是ai，合理，🤣)
            # 这里提供一个网站做测试，搜集了2022年的高考作文题    https://edu.gmw.cn/2022-06/08/content_35796045.htm
            # 如果把其中一题直接从网页上复制下来从QQ发送给机器人然后机器人发送给GPT，就会出现只发送一半的情况
            # 暂时没有解决办法
            chatgpt.send(msg=re.sub('\n+', '\n', str(user_msg).replace("\r","").replace("\u3000","")))
            user_msg = chatgpt.getLastReply()
            await word.finish(Message(f"[CQ:at,qq={uid}]{user_msg}"))
        await word.finish(Message(f"[CQ:at,qq={uid}]⚠️GPT可能在忙或者出错，请等待上一个人的问题生成完成或者刷新⌛"))



    #返回最后一次生成的
    returnReply_awake=on_keyword({"!b"},rule=to_me(),block=True,priority=11)
    @returnReply_awake.handle()
    async def _(event: GroupMessageEvent):
        uid=event.user_id
        msg = '这是最后一次提问GPT的回答📲:\n\n'
        await word.finish(Message(f"[CQ:at,qq={uid}]{msg}{chatgpt.getReplyList()}"))

    #刷新网页
    refreshGPT_awake=on_keyword({"!f5"},rule=to_me(),block=True,priority=11)
    @refreshGPT_awake.handle()
    async def _(event: GroupMessageEvent):
        uid=event.user_id
        chatgpt.open(refresh=True)
        time.sleep(2)
        GPTIO.log(chatgpt.GPT_status)
        chatgpt.GPT_status = chatgpt.gptBusyorFree()
        GPTIO.log(chatgpt.GPT_status)
        if( 'finish' in chatgpt.GPT_status):
            msg ='👌🔄刷新成功🔄👌'
        else:
            msg = '🤦‍♀️刷新失败,请继续刷新网页或者查看后台🤦‍♂️'
        await word.finish(Message(f"[CQ:at,qq={uid}]{msg}"))

    #查询GPT网页状态
    getGPTstatus_awake=on_keyword({"!st"},rule=to_me(),block=True,priority=11)
    @getGPTstatus_awake.handle()
    async def _(event: GroupMessageEvent):
        uid=event.user_id
        chatgpt.gptBusyorFree()
        await word.finish(Message(f"[CQ:at,qq={uid}]{str(chatgpt.GPT_status)}"))


    #菜单
    menu_awake=on_keyword({"!h"},rule=to_me(),block=True,priority=10)
    @menu_awake.handle()
    async def _(event: GroupMessageEvent):
        uid=event.user_id
        _a= '\n❓📖chatGPT机器人帮助菜单🧑‍💻\n'
        a = '❓!h     --帮助菜单\n'
        b = '↩️!b     --返回最后一次GPT的回答\n'
        c = '🔄!f5    --刷新网页\n'
        d = '📡!redo  --重新生成\n'
        e = '🧐!st    --查看GPT状态\n'
        menu_str = _a+a+b+c+d+e
        if(active_bowser):
            f = '🌐!boww  --使用浏览器提问!bww+空格+要问的问题\n'
            menu_str = menu_str + f
        await word.finish(Message(f"[CQ:at,qq={uid}]{menu_str}"))



