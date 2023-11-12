# 将原始数据建成一个完整数据库的模块

import os
import sqlite3
from Basic_Configuration import *


def merge_txt_files_into_database(folder_path, database):
    # 获取文件夹下所有txt文件并按照文件名排序
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

    # 一次性读取两个txt文件的内容并将它们逐行合并，同时将秒转换为时:分:秒格式，作为第三列
    for i in range(0, len(txt_files), 2):
        if i + 1 < len(txt_files):
            file1_path = os.path.join(folder_path, txt_files[i])
            file2_path = os.path.join(folder_path, txt_files[i + 1])

            with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
                content1 = file1.readlines()
                content2 = file2.readlines()

                timestamp_seconds = int(content1[0].strip())  # 假设时间戳在第一行

                for line1, line2 in zip(content1[1:], content2[1:]):
                    if line1.strip() and line2.strip():  # 检查行数据是否都存在
                        hours = timestamp_seconds // 3600
                        minutes = (timestamp_seconds % 3600) // 60
                        seconds = timestamp_seconds % 60

                        timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"
                        boat_name = folder_path[-5:]
                        category = categories[boat_name][i // 2]
                        fix_err = 1 + Errors[category]

                        x, y = (
                            float(line1.strip()) / fix_err,
                            float(line2.strip()) / fix_err,
                        )  # 修正后的x, y坐标

                        database.execute(
                            Insertion_Command, (boat_name, x, y, timestamp, category)
                        )  # 将数据输入到数据库中
                        timestamp_seconds += 1  # 每行时间戳递增1秒


# 用于将四艘船的数据全部导入一个数据库中， 包含每艘船的编码、(x, y)坐标对， 时间戳与数据源
def make_complete_database(path=Path_Of_Database):
    os.makedirs(f"{path}", exist_ok=True)
    file_name = f"{Name_Of_Database}.db"
    if file_name in os.listdir(path):
        os.remove(f"{path}/{file_name}")  # 如果已经有了同名数据库，将其删除之后重建数据库，否则程序会因存在相同数据库而报错
    db = sqlite3.Connection(f"{path}/{file_name}")
    db.execute(Initialize_Command)
    Boat_list = sorted(
        [
            f"./Origin_Data/{folder}"
            for folder in os.listdir(Path_Of_Data)
            if folder.startswith("boat")
        ]
    )
    for boat in Boat_list:
        merge_txt_files_into_database(boat, db)
    db.commit()  # 有这条命令才能生成实体数据库
    return db
