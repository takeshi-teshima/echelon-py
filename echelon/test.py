import numpy as np


def _mock_1dim_data():
    h = np.array([1, 2, 3, 4, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 1])
    W = np.zeros((25, 25), dtype='int8')
    W[np.eye(len(W), k=1, dtype='bool')] = 1
    W[np.eye(len(W), k=-1, dtype='bool')] = 1
    return h, W


def _mock_2dim_data():
    data = np.array([
        [2, 8, 24, 5, 3],
        [1, 10, 14, 22, 15],
        [4, 21, 19, 23, 25],
        [16, 20, 12, 11, 17],
        [13, 6, 9, 7, 18],
    ])
    n, m = data.shape
    W = np.zeros((n * m,)*2, dtype='int8')

    for i in range(len(W)):
        for delta in [-m, m]:
            j = i + delta
            if (0 <= j) and (j <= len(W)-1):
                W[i, j] = 1
        for delta in [-1, 1]:
            j = i + delta
            if (0 <= j) and (j <= len(W)-1):
                # If j does not move out to a different row
                if (i // m) == (j // m):
                    W[i, j] = 1

    return data, W


def _visualize_echelons(shape, peak_echelons, foundation_echelons):
    W = np.zeros(shape, dtype='int8')
    for i, echelon in enumerate(peak_echelons):
        for e in echelon:
            W[np.unravel_index(e, shape=W.shape)] = i + 1
    for i, echelon in enumerate(foundation_echelons):
        for e in echelon:
            W[np.unravel_index(e, shape=W.shape)] = len(peak_echelons) + i + 1
    return W
