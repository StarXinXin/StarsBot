# 发送信息API：
```python
await HotList.send(matched["Platform"], reply_message=True)
```
# 发送网络图片
```python
await Bing.finish(MessageSegment.image(str(image_url)), reply_message=True)
```
# 拼接文本
```python
await Bing.finish(
    MessageSegment.image(str(image_url) + 
    MessageSegment.text(str(image_url)), reply_message=True)
```
# 生成requirements.txt
```pip
pip freeze > requirements.txt
```