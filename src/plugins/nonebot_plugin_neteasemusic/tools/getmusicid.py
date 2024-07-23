import json
from nonebot.log import logger
def get_song_id_at_index(file_path, index):
    """
    从 JSON 文件中获取指定索引的 ID
    :param file_path: JSON 文件路径
    :param index: 要获取的 ID 的索引
    """
    try:
        # 读取 JSON 文件
        with open(file_path, 'r') as f:
            song_ids = json.load(f)

            # 检查索引是否有效
            if 0 <= index < len(song_ids):
                return song_ids[index]
            else:
                return None  # 如果索引超出范围，返回 None 或者抛出异常
    except FileNotFoundError:
        logger.log(f"未找到文件：{file_path}")
        return None
    except json.JSONDecodeError:
        logger.log(f"从文件解码 JSON 时出错：{file_path}")
        return None
    except Exception as e:
        logger.log(f"发生错误： {e}")
        return None
