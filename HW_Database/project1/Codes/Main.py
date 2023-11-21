from Get_Database import *
from Basic_Configuration import *
from Data_Analysis import *

database = make_complete_database()  # 生成完整的数据库

# 对于想要查看的船只，将对应编号修改为True:
Interested_boat = {
    1: True,
    2: False,
    3: False,
    4: True,
}

# 对于想要查看的检测数据，将对应项修改为True:
Interested_spectrum = {
    "Far": False,
    "Middle": True,
    "Near": False,
    "Full": True,
}

Get_Pictures(
    database, Interested_boat, Interested_spectrum, show_fixed_track=True
)  # 最后一个参数，如果不想在图像上显示拟合后的曲线，True改成False即可

plt.show()  # 显示图像
