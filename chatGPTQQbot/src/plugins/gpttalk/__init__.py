from nonebot import on_keyword
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.rule import to_me
from js import GPTIO
import time
import re
chatgpt = GPTIO.ChatGPT()
chatgpt.init(9222)
chatgpt.open()


word=on_keyword({"在吗"},rule=to_me(),block=True,priority=12)
@word.handle()
async def _(event: GroupMessageEvent):
    uid=event.user_id
    msg = "好👌"
    await word.finish(Message(f"[CQ:at,qq={uid}]{msg}"))

#向GPT发送消息
askGPT_awake=on_message(rule=to_me(),priority=100)
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
    e = '🧐!st    --查看GPT状态'
    await word.finish(Message(f"[CQ:at,qq={uid}]{_a+a+b+c+d+e}"))
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




