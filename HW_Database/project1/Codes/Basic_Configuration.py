# 这个模块里是这个项目通用的一些配置参数，有想要改动的基本都可以通过修改这里的参数实现

categories = {
    "boat1": ["camera1", "camera2", "camera3", "radar"],
    "boat2": ["camera1", "camera2", "camera3", "radar"],
    "boat3": ["camera1", "camera2", "camera3", "radar"],
    "boat4": ["camera1", "camera2", "radar"],
}  # 用于表示每艘船的数据来源

Errors = {"camera1": -0.2218, "camera2": 0, "camera3": 0.065, "radar": 0}

Name_Of_Database = "BoatData"  # 数据库名称

Path_Of_Database = ".."  # 数据库存储路径（默认为当前路径）

Path_Of_Data = "../Origin_Data"  # 数据集所在路径（默认为存在同一路径下的Origin_Data文件夹中）

Initialize_Command = (
    f"CREATE TABLE {Name_Of_Database}(BoatName, x, y, Timestamp, Source);"  # 初始化数据库的命令
)

Insertion_Command = f"INSERT INTO {Name_Of_Database} VALUES (?, ?, ?, ?, ?);"  # 添加数据的命令

Ranges = {
    "Far": (-3000, -1500),
    "Middle": (-1500, 0),
    "Near": (0, 500),
    "Full": (-3000, 500),
}  # 用于划分不同的检测范围

Y_Limit = {
    "Far": (-1500, 0),
    "Middle": (-600, 0),
    "Near": (-600, 0),
    "Full": (-1500, 0),
}

Track_Line_Config = {
    "camera1": "k",
    "camera2": "g",
    "camera3": "b",
    "radar": "y",
}  # 画图时的线型设置

Fixed_Line_Config = "r--"  # 拟合轨迹线型设置
