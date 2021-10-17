import numpy as np
import pandas as pd
from dataclasses import dataclass

from .algorithms import find_peak_echelons, find_foundation_echelons, find_echelon_clusters
from .oracle import EchelonOracleBase, NdarrayEchelonOracle

## Type hinting
from typing import Tuple, List
IndexSetType = List[int]
EchelonType = IndexSetType
EchelonsType = List[EchelonType]
NeighborsType = List[IndexSetType]


@dataclass
class Result_EchelonAnalysis:
    """Class for keeping the results of echelon analysis."""
    peak_echelons: EchelonsType
    foundation_echelons: EchelonsType
    oracle: EchelonOracleBase

@dataclass
class Result_EchelonCluster:
    table: object


class EchelonAnalysis:
    def cluster(self, result: Result_EchelonAnalysis) -> Result_EchelonCluster:
        """
        Examples:
            >>> from .test import _mock_1dim_data
            >>> h, W = _mock_1dim_data()
            >>> analyzer = EchelonAnalysis()
            >>> result = analyzer(h, W)
            >>> analyzer.cluster(result).table
              representatives                               indices
            0            [16]  [16, 17, 15, 14, 18, 19, 20, 21, 22]
            1            [13]               [13, 12, 14, 11, 10, 9]
            2             [6]                    [6, 5, 7, 4, 8, 9]
            3             [3]                       [3, 2, 4, 1, 0]
            4            [23]                          [23, 22, 24]
        """
        clusters = find_echelon_clusters(result.peak_echelons, result.foundation_echelons, result.oracle)
        echelon_clusters = []
        for cluster in clusters:
            _argmax, _ = result.oracle.max_indices(cluster)
            echelon_clusters.append((_argmax, cluster))
        echelon_cluster_table = pd.DataFrame(echelon_clusters, columns =['representatives', 'indices'])
        return Result_EchelonCluster(
            table=echelon_cluster_table
        )

    def __call__(self, data: np.ndarray, adjacency: np.ndarray) -> Result_EchelonAnalysis:
        """
        Params:
            data: 1-dimensional data of realized values.
            adjacency: size-$len(data)$ square array of adjacency.

        Examples:
            >>> from .test import _mock_1dim_data
            >>> h, W = _mock_1dim_data()
            >>> result = EchelonAnalysis()(h, W)
            >>> result.peak_echelons
            [[16, 17, 15], [13], [6, 5, 7], [3], [23]]
            >>> result.foundation_echelons
            [[12, 14, 18, 19, 11, 10, 20], [2, 4, 8], [1, 9, 21], [0, 22, 24]]
        """
        oracle = NdarrayEchelonOracle(data, adjacency)
        peak_echelons = find_peak_echelons(oracle)
        foundation_echelons = find_foundation_echelons(oracle, peak_echelons)
        return Result_EchelonAnalysis(
            peak_echelons=peak_echelons,
            foundation_echelons=foundation_echelons,
            oracle=oracle
        )


class OneDimEchelonAnalysis(EchelonAnalysis):
    def __call__(self, data: np.ndarray) -> Result_EchelonAnalysis:
        """
        Params:
            data: 1-dimensional data of realized values.

        Examples:
            >>> from .test import _mock_1dim_data
            >>> h, _ = _mock_1dim_data()
            >>> result = OneDimEchelonAnalysis()(h)
            >>> result.peak_echelons
            [[16, 17, 15], [13], [6, 5, 7], [3], [23]]
            >>> result.foundation_echelons
            [[12, 14, 18, 19, 11, 10, 20], [2, 4, 8], [1, 9, 21], [0, 22, 24]]
        """
        W = np.zeros((len(data),)*2, dtype='int8')
        W[np.eye(len(W), k=1, dtype='bool')] = 1
        W[np.eye(len(W), k=-1, dtype='bool')] = 1
        return super().__call__(data, W)
