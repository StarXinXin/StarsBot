# 群白名单和管理员白名单

主要是怕非使用群，误触发机器人的关键词

如果群不在白名单中就不会有响应

对应的文件是[AdminTool.py](https://github.com/StarXinXin/StarsBot/blob/master/utils/AdminTool.py)

管理员白名单是负责判定是否有能力去添加群白名单

你也可以直接在[AdminTool.py](https://github.com/StarXinXin/StarsBot/blob/master/utils/AdminTool.py)文件里面先定义管理员QQ号，并删除掉现有的Profile文件夹，它会自动初始化
## 文档

See [Docs](https://github.com/StarXinXin/StarsBot/blob/master/utils/AdminTool%E4%BD%BF%E7%94%A8.md)

# 添加群

## 使用示例

### 添加群白名单

```python
/添加群白名单
```

如果你在群聊中,插件会自动识别群号，并添加进白名单

如果你是在单人聊天里面设置，可使用以下指令

```python
/添加群白名单+空格+群号
```

```python
/添加群白名单+群号
```

### 移除群白名单

同上面的添加群白名单，将添加群白名单改成移除群白名单

# 添加管理员

添加管理员不会自动识别，只能指定

## 使用示例

### 添加管理员

```python
/添加管理员+空格+管理员QQ号
```

```python
/添加管理员+管理员QQ号
```

### 移除管理员

```python
/移除管理员+空格+管理员QQ号
```

```python
/移除管理员+管理员QQ号
```