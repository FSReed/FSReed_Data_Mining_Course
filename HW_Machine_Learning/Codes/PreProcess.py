import pandas as pd
import numpy as np

DATA_PATH = "Data/"

Dictionary2 = {
    "Cantilever": 1,
    "Double curvature": 2,
    "Circular": 1,
    "Octagonal": 2,
    "Spiral": 2,
    "Flexure": 1,
    "Flexure-shear": 2,
    "Shear": 3,
}

Dictionary5 = {"S": 1, "R": 2}


def getData(path=DATA_PATH, file_num=1):
    file = f"{DATA_PATH}{file_num}.xlsx"
    print(f"Working on File: {file}")
    if file_num != 6:
        header = 0
    else:
        header = 1
    df = pd.read_excel(file, header=header)
    origin_nparray = df.to_numpy()
    X_train = origin_nparray[:, 1:-1]
    y_train = origin_nparray[:, -1]
    if file_num == 2:
        for position in range(X_train.shape[0]):
            X_train[position, 0] = Dictionary2[X_train[position, 0]]
            X_train[position, 1] = Dictionary2[X_train[position, 1]]
            X_train[position, 2] = Dictionary2[X_train[position, 2]]
            y_train[position] = Dictionary2[y_train[position]]
    elif file_num == 5:
        for position in range(X_train.shape[0]):
            X_train[position, -1] = Dictionary5[X_train[position, -1]]
    float_X_train = np.zeros(X_train.shape)

    # 为了线性回归时特征归一化方便，将所有得到的数据集数据转化为float类型
    for row in range(X_train.shape[0]):
        for column in range(X_train.shape[1]):
            float_X_train[row, column] = (float)(X_train[row, column])
    print("Get the dtype=float data matrix.")
    return (float_X_train, y_train)