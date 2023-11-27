import numpy as np


# The new_features function is used only for dataset 1.
FEATURE_AMOUNT = 11


def new_features(X_origin):
    m, n = X_origin.shape
    new_features = np.zeros((m, FEATURE_AMOUNT))
    new_features[:, :7] = np.copy(X_origin[:, :7])
    new_features[:, 7] = np.copy(X_origin[:, 7] * X_origin[:, 8])
    for position in range(m):
        if X_origin[position, 9] != 0:
            new_features[position][8] = (
                X_origin[position, 9] * X_origin[position, 11] / X_origin[position, 10]
            )
        if X_origin[position, 12] != 0:
            new_features[position][9] = (
                X_origin[position, 12] * X_origin[position, 14] / X_origin[position, 13]
            )
    new_features[:, 10] = np.copy(X_origin[:, 15])
    return new_features
