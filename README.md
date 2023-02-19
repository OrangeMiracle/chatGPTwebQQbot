# 把chatGPT部署到你的QQ
这个项目是一个基于nonebotv2开发的插件，需要配合go-cqhttp登陆QQ机器人，成功绕过网页端检测，能够把chatGPT部署到QQ

🙏🙏🙏🤗首先，十分感谢Bilibili的这位up提供的核心思路以及示例代码 @蒙舌上単

大佬的空间     https://space.bilibili.com/3493075036932748/
大佬提供的代码 https://www.bilibili.com/read/cv20610733?spm_id_from=333.999.0.0

本项目基于

Nonebot官网:      https://v2.nonebot.dev/

go-cqhttp官网:    https://docs.go-cqhttp.org/

Reverse Engineered ChatGPT API:     https://github.com/acheong08/ChatGPT

献丑了😅，家人们，我python是现学的，做这个项目的时候刚自学py不到4天(2023.1.13开始学)，怎么使用Github也是现学的，如果出现任何问题，请在issue中提问🤷

目前功能

1.支持选择打开网页或者不打开网页登陆账号（如果选择启用 “需要打开网页的功能” 这个功能只能登陆一个账号，但是可以与 ”不打开网页登陆账号“ 的功能同时存在

2.多人同时提问

3.多账号支持

4.绕过网页检测

5.每个人可以用一个单独的对话框

==========💬一些废话💬==========

隔壁大佬做的

https://www.bilibili.com/video/BV1Mx4y1c718/?spm_id_from=333.788.header_right.history_list.click&vd_source=204ca2d530f8a482c037153b136d1b0b

值得一提的是，他的项目使用了mirai作为QQ登陆器，我使用mirai登陆QQ一段时间之后会显示“QQ版本过低，无法登录QQ，请更新到最新版本”，同时这个无法登陆的QQ号会在所有没有更新到最新版的QQ的设备上面同时出现这个问题，安卓，PC，macos，iphone，全部同时出现无法登录的错误。所以我在这个项目里面使用了go-cqhttp作为QQ登陆器。不过我这个是模拟人工点击，理论上不会被GPT封堵。请根据自己的情况选择合适的机器人

==============================

❓已知问题请查看issue部分

❔如何运行&部署

1.🖥️确认你的运行环境

    在开始之前，你将会需要
  
      1)🏠一个Windows系统   (如果你想要使用其他系统的话，请确保能够打开chrome浏览器，并且python能够通过selenium库操作浏览器)
      
        如果你选择一直都不启用 “需要打开网页的功能” 那理论上可以在命令行终端运行
  
      2)🐍一个python环境
  
      3)🆔chatGPT账号以及能够使用chatGPT的梯子


2.⚙️如何配置

    如果你打算直接运行我这个github项目，就可以跳过 "安装Nonebotv2" 这一步

  1)🛠️安装Nonebotv2，这里有一些安装教程，不再过多赘述
  
    https://v2.nonebot.dev/docs/start/installation
  
    https://www.bilibili.com/video/BV1984y1b7JY?p=2&share_source=copy_web
  
    ❗❗在安装时，请把插件保存目录放到src文件夹中
  
  2)🛠️安装go-cqhttp(你也可以使用Nonebot中的go-cqhttp插件)
    
    这里是官方教程
    
    https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B
    
    在以上两项都安装完成并进行基础配置，确保他们能够互相通信
    
  3)🐍配置虚拟环境
  
    在启动bot之前，请先进入Nonebot为你生成的虚拟环境，添加以下的包
    
      pip install html
    
      pip install selenium
      
      pip install aiocqhttp
      
      pip install sqlite3
      
      如果出现安装失败可以试试替换pip为pip3，如果还是失败，请在issue提出
    
  4)💾安装插件
  
    在我的github项目中找到  chatGPTwebQQbot/chatGPTQQbot/src/plugins/gpttalk/
    
    把整个gpttalk文件夹放进你刚刚创建的Nonebot机器人的  ./<你机器人的名字>/src/plugins   文件夹中
    
    在我的github项目中找到  chatGPTwebQQbot/chatGPTQQbot/js
    
    把整个js文件夹放进你刚刚创建的Nonebot机器人的  ./<你机器人的名字>/   文件夹中
    
    填写你的账号到js文件夹下的ghotmail_account.csv和user_account.csv
    
    user_account.csv对应使用邮箱登陆的账号
    
    ghotmail_account.cs对应使用 __Secure-next-auth.session-token    登陆的账号
    
    请根据文件夹中提供的格式进行填写，注意逗号要用英文逗号，以及最顶上的列名不可删除，每个账号占用一行，请手动回车换行,plus_status根据你这个账号有没有充值plus版，有就填true，没有就false
  
  5)🚀启动
    
    1.🌟挂上你的梯子进行魔法上网
    
    2.🌏使用项目中附带的chatGPT.lnk打开谷歌浏览器，并且打开GPT页面，登陆你自己的chatGPT账号    （如果没有开启 “需要打开网页的功能” 这个功能, 请忽略这一步）
    
      一定要用附带的谷歌浏览器快捷方式先手动打开chatGPT网页版，并且登录你自己的账号
      
      (这个chatGPT.lnk是chrome浏览器的快捷方式，但是添加了一些参数，你再打开之前应该把 “右键->属性” 其中指向chrome.exe的地址改成你自己电脑上chrome.exe的地址)
    
    3.🚀启动go-cqhttp
    
    4.🚀🐍💻进入机器人所在的文件夹，并启动机器人生成时候自动创建的虚拟环境，在虚拟环境中启动Nonebot
    
    ✅完成🎉🎉🎉
    
    使用  @机器人!h 来发送菜单    如果没有学则开启 “需要开启浏览器的功能” 菜单也就没用啦




