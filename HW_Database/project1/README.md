# 数据库大作业

## 作业概况

本次作业选择了project1, 其中包含的主要文件有：

- `Codes/Main.py`, 实际执行的文件
- `Codes/Basic_COnfiguration.py`， 用于配置数据库以及作图的基本信息
- `Codes/Get_Database.py`， 用于生成数据库`BoatData.db`
- `Codes/Data_Analysis.py`， 用于处理数据库中的数据并且作图
- `BoatData.db`， 是由`Main.py`生成的数据库文件，在`Codes/Get_Database.py`中进行了设置，以防止重复运行`Main.py`时因数据库已存在而报错

## 使用方法

在`Codes/Main.py`中修改调查的船只、检测的距离范围等数据，然后直接运行`Main.py`即可获得需要的图像

## 数据处理方法

- 在将原始数据输入数据库时，已经根据各个机位给出的误差进行了修正
- 得到拟合轨迹的方法就是将同一时刻的坐标求均值，得到一系列新的坐标，据此作图

初始设置是绘制1、4号船的Middle、Full轨迹，共四张图，效果图已经附在作业包`Figures/`文件夹中
