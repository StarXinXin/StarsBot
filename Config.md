![StarsBot](https://socialify.git.ci/StarXinXin/StarsBot/image?forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F118031165%3Fv%3D4&name=1&owner=1&stargazers=1&theme=Light)

# 简介

## 欢迎来到 `星辰Bot` 项目！这是一款基于 Nonebot2 打造的智能 QQ 机器人，旨在为用户提供丰富的功能体验。无论是获取一言的灵感，探索历史上的今天，还是穿梭60s世界，`星辰Bot` 为您打开了全新的交流之门。快来尝试吧！

# 文档
### [返回 README.md](README.md)

### [Nonebot Docs](https://nonebot.dev/)

# 配置
可运行根目录下的Main.py (还没写[Doge]) 文件，初始化配置文件
# 其他
.env 这些类似的文件，别忘了配置了啊！！！！！！！！ 
### [API.md](API.md)
这个文件是我收集的一些请求方法，一开始写这些功能的时候难到了我，我就记录了一下

没有做过多的解释，毕竟当时想我看得懂就好[Doge]
# 相关文件介绍
群白名单文件路径(如果没有文件，请自己手动写入文件)
```
Profile/Whitelist/GroupWhitelist.json
```
格式
```
["群号ID", "群号ID"]
```

管理员白名单文件路径(如果没有文件，请自己手动写入文件)
```
Profile/Whitelist/AdminWhitelist.json
```
格式
```
["管理员QQ号", "管理员QQ号"]
```

初始化以上两个文件以后，可在群聊或私聊中发送指令：
```
/白名单配置
```
使用相关的指令进行配置即可

# 管理员须知菜单指令
```
/运行状态
```
```
/群管菜单
```
# 你可能会看到的其他的路径
### 菜单配置路径
```
Profile/Menu/
```
这个路径还是挺重要的，这个路径下存放了菜单配置文件，大白话：管理菜单的内容，包括游戏菜单和默认菜单
### 整点报时路径
```
Profile/Timing/TimeOnHour
```
### AI聊天历史记录路径
```
Profile/Chat/
```
### 游戏功能数据路径
```
Profile/GameData/
```
