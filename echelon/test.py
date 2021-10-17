import numpy as np


def _mock_1dim_data():
    h = np.array([1, 2, 3, 4, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 1])
    W = np.zeros((25, 25), dtype='int8')
    W[np.eye(len(W), k=1, dtype='bool')] = 1
    W[np.eye(len(W), k=-1, dtype='bool')] = 1
    return h, W
