import asyncio
from nonebot.log import logger
import os
import httpx
import aiofiles
from nonebot_plugin_alconna import UniMessage
from tqdm.asyncio import tqdm as atqdm


async def download_file(url, save_to, filename):
    """
    异步下载文件并保存到指定位置。
    ...
    """
    full_path = os.path.join(save_to, filename)

    os.makedirs(save_to, exist_ok=True)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 256  # 减小数据块大小
            progress_bar = atqdm(total=total_size, unit="B", unit_scale=True)

            async with aiofiles.open(full_path, "wb") as f:
                # await UniMessage("服务器处理中").send(reply_to=True)
                async for chunk in response.aiter_bytes(block_size):
                    await f.write(chunk)
                    progress_bar.update(len(chunk))
                    await asyncio.sleep(0)  # 强制事件循环处理其他任务

            progress_bar.close()
            print(f"文件已成功下载至 {full_path}")
            return full_path
    except Exception as e:
        print(f"下载文件时发生错误：{e}")
        return ""
    except httpx.ConnectTimeout as e:
        await UniMessage("请求超时,主机网络异常").send(reply_to=True)
        return ""

# # 使用示例
# async def main():
#     file_path = await download_file('https://example.com/large_file.zip', './Download/Music', 'Music.mp3')
#     print(file_path)
#
# # 运行示例
# asyncio.run(main())
