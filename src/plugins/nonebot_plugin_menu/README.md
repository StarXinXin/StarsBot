# 菜单

菜单是机器人的一个核心功能，也是机器人最常用的功能之一。

## 添加菜单

```python
await UniMessage("欢迎使用星辰Bot\n"
                 "发送以下指令，获取更多哦~\n\n"
                 "/一言\n"
                 "/60s世界\n"
                 "/管理员菜单").send(reply_to=true)
```

看代码应该懂了吧，这个我也不好解释


| 触发词 | 介绍     |
| ------ |--------|
| /菜单  | 获取菜单列表 |