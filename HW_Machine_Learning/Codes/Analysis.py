from ZScore import zScoreNormalize
from sklearn.model_selection import train_test_split
import numpy as np

maxLoop = 100  # 模型拟合的次数，可以调整


def Regressor(X_origin, y_origin, method):
    X_train, X_test, y_train, y_test = train_test_split(
        X_origin, y_origin, test_size=0.3
    )
    X_train, mu, sigma = zScoreNormalize(
        X_train
    )  # 因为提取数据的时候已经进行了float类型转换，所以特征归一化对所有数据集都适用
    reg = method(max_features="sqrt").fit(X_train, y_train)
    # 注意上面一行，里面的参数是用于随机森林模型调参的，用另外两个模型会报错

    X_pred = (X_test - mu) / sigma
    R = reg.score(X_pred, y_test)
    weights = reg.feature_importances_
    return (R, weights)


def filtFeature(X_origin, y_origin, model):
    print(f"Using model: {model}")
    N, p = X_origin.shape
    R_values = []
    Adjusted_R_values = []
    weights = np.zeros(X_origin.shape[1])
    for i in range(maxLoop):
        R, currentImportance = Regressor(X_origin, y_origin, method=model)
        R_values.append(R)
        Adj_R = 1 - (1 - R**2) * (N - 1) / (N - p - 1)
        Adjusted_R_values.append(Adj_R)
        weights = weights + currentImportance
    avgRValue = sum(R_values) / len(R_values)
    avgAdjR = sum(Adjusted_R_values) / len(Adjusted_R_values)
    weights = weights / maxLoop
    print(f"average R in {maxLoop} loops is {avgRValue}")
    print(f"Max R is: {max(R_values)}, Min R is: {min(R_values)}")
    print(f"average Adj_R in {maxLoop} loops is {avgAdjR}")
    print(
        f"Max Adj_R is: {max(Adjusted_R_values)}, Min Adj_R is: {min(Adjusted_R_values)}"
    )
    print(f"The importances of all features are: {weights}")
    return weights
