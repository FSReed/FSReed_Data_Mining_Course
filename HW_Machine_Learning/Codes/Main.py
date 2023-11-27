from PreProcess import *
from Features import *
from Analysis import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

X_origin, y_origin = getData(file_num=5)  # 修改file_num值可以拟合不同的模型
# X_origin = new_features(X_origin) # 这条命令只对第一个数据集有效，是用于特征重组的
weights = filtFeature(
    X_origin, y_origin, model=RandomForestRegressor
)  # 改变model值可以用不同的模型拟合
