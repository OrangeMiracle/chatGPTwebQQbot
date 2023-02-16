# 把chatGPT部署到你的QQ
这个项目是一个基于nonebotv2开发的插件，需要配合go-cqhttp登陆QQ机器人，成功绕过网页端检测，能够把chatGPT部署到QQ

🙏🙏🙏🤗首先，十分感谢Bilibili的这位up提供的核心思路以及示例代码 @蒙舌上単

大佬的空间     https://space.bilibili.com/3493075036932748/
大佬提供的代码 https://www.bilibili.com/read/cv20610733?spm_id_from=333.999.0.0

Nonebot官网:      https://v2.nonebot.dev/
go-cqhtth官网:    https://docs.go-cqhttp.org/

献丑了😅，家人们，我python是现学的，做这个项目的时候刚自学py不到4天(2023.1.13开始学)，怎么使用Github也是现学的，如果出现任何问题，请在issue中提问🤷

❓已知问题请查看issue部分

❔如何运行&部署

1.🖥️确认你的运行环境

    你将会需要
  
      1)🏠一个Windows系统   (如果你想要使用其他系统的话，请确保能够打开chrome浏览器，并且python能够通过selenium库操作浏览器)
  
      2)🐍一个python环境
  
      3)🆔chatGPT账号以及能够使用chatGPT的梯子


2.⚙️如何配置

  1)🛠️安装Nonebotv2，这里有一些安装教程，不再过多赘述
  
    https://v2.nonebot.dev/docs/start/installation
  
    https://www.bilibili.com/video/BV1984y1b7JY?p=2&share_source=copy_web
  
    ❗❗在安装时，请把插件保存目录放到src文件夹中
    
    如果你打算直接运行我这个github项目，就可以跳过这一步
  
  2)🛠️安装go-cqhttp(你也可以使用Nonebot中的go-cqhttp插件)
    
    这里是官方教程
    
    https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B
    
    在以上两项都安装完成并进行基础配置，确保他们能够互相通信
    
  3)🐍配置虚拟环境
  
    在启动bot之前，请先进入Nonebot为你生成的虚拟环境，添加以下的包
    
      pip install html
    
      pip install selenium
    
  4)💾安装插件
  
    在我的github项目中找到  chatGPTwebQQbot/chatGPTQQbot/src/plugins/gpttalk/
    
    把整个gpttalk文件夹放进你刚刚创建的Nonebot机器人的  ./<你机器人的名字>/src/plugins   文件夹中
    
    在我的github项目中找到  chatGPTwebQQbot/chatGPTQQbot/js
    
    把整个js文件夹放进你刚刚创建的Nonebot机器人的  ./<你机器人的名字>/   文件夹中
  
  5)🚀启动
    
    1.🌟挂上你的梯子进行魔法上网
    
    2.🌏使用项目中附带的chatGPT.lnk打开谷歌浏览器，并且打开GPT页面，登陆你自己的chatGPT账号
    
      一定要用附带的谷歌浏览器快捷方式先手动打开chatGPT网页版，并且登录你自己的账号
    
    3.🚀启动go-cqhttp
    
    4.🚀启动Nonebot
    
    ✅完成🎉🎉🎉
    
    使用  @机器人!h 来发送菜单




