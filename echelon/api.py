import numpy as np
import pandas as pd
from dataclasses import dataclass

from echelon.algorithms import (find_peak_echelons,
                                find_foundation_echelons,
                                find_echelon_clusters,
                                find_echelon_hierarchy,
                                find_echelon_hotspots
                                )
from echelon.oracle import EchelonOracleBase, NdarrayEchelonOracle, DataFrameEchelonOracle
from echelon.scan_oracle import ScanOracleBase, NdarrayScanOracle, DataFrameScanOracle

## Type hinting
from typing import Tuple, List, Union, Any, Dict
from anytree import Node
IndexSetType = List[int]
EchelonType = IndexSetType
EchelonsType = List[EchelonType]
NeighborsType = List[IndexSetType]


@dataclass
class Result_EchelonAnalysis:
    """Class for keeping the results of echelon analysis.

    Parameters:
        peak_echelons: list of peak echelons.
        foundation_echelons: list of foundation echelons.
        hierarchy_tree: root node (``anytree.Node``) of the hierarchy tree of the echelons.
        oracle: the oracle that is internally constructed during the instantiation of the analysis. Mainly for debugging purposes.

    Note:
        Each echelon is a list of indices of the original data.
    """
    peak_echelons: EchelonsType
    foundation_echelons: EchelonsType
    hierarchy_tree: Node
    oracle: EchelonOracleBase

    @property
    def echelons(self) -> EchelonsType:
        return self.peak_echelons + self.foundation_echelons


@dataclass
class Result_EchelonCluster:
    table: object


class EchelonAnalysis:
    def cluster(self, result: Result_EchelonAnalysis) -> Result_EchelonCluster:
        """
        Examples:
            >>> from echelon.test import _mock_1dim_data
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

    def dendrogram(self, result: Result_EchelonAnalysis,
                   plot_config_dict: dict=dict(num_linespace = 1)) -> str:
        """Draw a simple dendrogram-like figure of the echelon hierarchy.

        Parameters:
            result : the result object of the echelon construction.
            plot_config_dict : the dictionary to configure the visualization.
        """
        from anytree import RenderTree

        root = result.hierarchy_tree
        echelons = result.echelons

        def _default_echelon_to_str(echelon_id, _echelon, _max_idx, value, plot_config_dict):
            """Default function to convert echelon information to a string."""
            idx_map = plot_config_dict.get('idx_map', str)
            representatives = ",".join(map(idx_map, _max_idx))
            echelon_contents = ', '.join(map(idx_map, reversed(_echelon)))
            return f'E{echelon_id+1}({representatives}): [{echelon_contents}]\n (max: {value})' + '\n' * plot_config_dict.get('num_linespace', 0)

        def echelon_to_label(echelon_id):
            _echelon = echelons[echelon_id]
            _max_idx, value = result.oracle.max_indices(_echelon)
            _echelon_to_str = plot_config_dict.get('_echelon_to_str', _default_echelon_to_str)
            return _echelon_to_str(echelon_id, _echelon, _max_idx, value, plot_config_dict)

        return RenderTree(root).by_attr(lambda node: echelon_to_label(node.name))

    def echelon_hotspots(self, result: Result_EchelonAnalysis, scan_oracle: ScanOracleBase):
        hotspots = find_echelon_hotspots(scan_oracle,
                                            result.hierarchy_tree,
                                            result.echelons,
                                            result.oracle)
        return hotspots

    def _run_analysis(self, oracle: EchelonOracleBase) -> Result_EchelonAnalysis:
        peak_echelons = find_peak_echelons(oracle)
        foundation_echelons = find_foundation_echelons(oracle, peak_echelons)
        hierarchy = find_echelon_hierarchy(peak_echelons, foundation_echelons, oracle)
        return Result_EchelonAnalysis(
            peak_echelons=peak_echelons,
            foundation_echelons=foundation_echelons,
            hierarchy_tree = hierarchy,
            oracle=oracle
        )


    def __call__(self, data: np.ndarray, adjacency: np.ndarray) -> Result_EchelonAnalysis:
        """
        Parameters:
            data: 1-dimensional data of realized values.
            adjacency: size-$len(data)$ square array of adjacency.

        Examples:
            >>> from echelon.test import _mock_1dim_data
            >>> h, W = _mock_1dim_data()
            >>> result = EchelonAnalysis()(h, W)
            >>> result.peak_echelons
            [[16, 17, 15], [13], [6, 5, 7], [3], [23]]
            >>> result.foundation_echelons
            [[12, 14, 18, 19, 11, 10, 20], [2, 4, 8], [1, 9, 21], [0, 22, 24]]
        """
        oracle = NdarrayEchelonOracle(data, adjacency)
        return self._run_analysis(oracle)


class NdarrayEchelonAnalysis(EchelonAnalysis):
    def echelon_hotspots(self, result: Result_EchelonAnalysis, total_count_data, marked_count_data):
        scan_oracle = NdarrayScanOracle(total_count_data, marked_count_data)
        return super().echelon_hotspots(result, scan_oracle)


class OneDimEchelonAnalysis(NdarrayEchelonAnalysis):
    def __call__(self, data: np.ndarray) -> Result_EchelonAnalysis:
        """
        Parameters:
            data: 1-dimensional data of realized values.

        Examples:
            >>> from echelon.test import _mock_1dim_data, _visualize_echelons
            >>> h, _ = _mock_1dim_data()
            >>> result = OneDimEchelonAnalysis()(h)
            >>> result.peak_echelons
            [[16, 17, 15], [13], [6, 5, 7], [3], [23]]
            >>> result.foundation_echelons
            [[12, 14, 18, 19, 11, 10, 20], [2, 4, 8], [1, 9, 21], [0, 22, 24]]
            >>> print(h)
            [1 2 3 4 3 4 5 4 3 2 3 4 5 6 5 6 7 6 5 4 3 2 1 2 1]
            >>> print(_visualize_echelons(h.shape, result.peak_echelons, result.foundation_echelons))
            [9 8 7 4 7 3 3 3 7 8 6 6 6 2 6 1 1 1 6 6 6 8 9 5 9]
        """
        W = np.zeros((len(data),)*2, dtype='int8')
        W[np.eye(len(W), k=1, dtype='bool')] = 1
        W[np.eye(len(W), k=-1, dtype='bool')] = 1
        return super().__call__(data, W)


class TwoDimEchelonAnalysis(NdarrayEchelonAnalysis):
    """The standard API for two-dimensional matrix-shaped data.
    The API constructs the canonical adjacency matrix (i.e., the 4- or 8-neighborhood).
    """
    def __init__(self, adjacency_type='4'):
        super().__init__()
        if adjacency_type in ['4', '8']:
            self.adjacency_type = adjacency_type
        else:
            raise ValueError('Only 4 or 8 is allowed.')

    def _canonical_twodim_adjacency_4(self, n, m):
        """Construct the canonical adjacency matrix for two-dimensional data.
        The adjacency matrix is for the canonical 4-neighbors (up down left right;
        known as *von Neumann* neighborhood).

        Example:
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_4(2, 2)[0].reshape(2, 2))
            [[0 1]
             [1 0]]
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_4(3, 3)[4].reshape(3, 3))
            [[0 1 0]
             [1 0 1]
             [0 1 0]]
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_4(3, 3)[5].reshape(3, 3))
            [[0 0 1]
             [0 1 0]
             [0 0 1]]
        """
        W = np.zeros((n * m,)*2, dtype='int8')

        for i in range(len(W)):
            for delta in [-m, m]:
                j = i + delta
                if (0 <= j) and (j <= len(W)-1):
                    W[i, j] = 1
            for delta in [-1, 1]:
                j = i + delta
                # If j does not move out to a different row
                if (0 <= j) and (j <= len(W)-1) and ((i // m) == (j // m)):
                    W[i, j] = 1
        return W

    def _canonical_twodim_adjacency_8(self, n, m):
        """Construct the canonical adjacency matrix for two-dimensional data.
        The adjacency matrix is for 8-neighbors (up down left right, and their combinations;
        known as *Moore* neighborhood).

        Example:
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_8(2, 2)[0].reshape(2, 2))
            [[0 1]
             [1 1]]
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_8(3, 3)[4].reshape(3, 3))
            [[1 1 1]
             [1 0 1]
             [1 1 1]]
            >>> print(TwoDimEchelonAnalysis()._canonical_twodim_adjacency_8(3, 3)[3].reshape(3, 3))
            [[1 1 0]
             [0 1 0]
             [1 1 0]]
        """
        W = np.zeros((n * m,)*2, dtype='int8')

        for i in range(len(W)):
            for delta in [-m-1, -m, -m+1]:
                j = i + delta
                if (0 <= j) and (j <= len(W)-1) and ((i // m) == (j // m + 1)):
                    # If j does not move out to a different row
                    W[i, j] = 1
            for delta in [m-1, m, m+1]:
                j = i + delta
                if (0 <= j) and (j <= len(W)-1) and ((i // m) == (j // m - 1)):
                    # If j does not move out to a different row
                    W[i, j] = 1
            for delta in [-1, 1]:
                j = i + delta
                if (0 <= j) and (j <= len(W)-1) and ((i // m) == (j // m)):
                    # If j does not move out to a different row
                    W[i, j] = 1
        return W

    def __call__(self, data: np.ndarray) -> Result_EchelonAnalysis:
        """
        Parameters:
            data: 2-dimensional data of realized values.

        Examples:
            >>> from echelon.test import _mock_2dim_data, _visualize_echelons
            >>> data, _ = _mock_2dim_data()
            >>> result = TwoDimEchelonAnalysis()(data)
            >>> result.peak_echelons
            [[14, 13, 8], [2], [11, 16], [24]]
            >>> result.foundation_echelons
            [[12], [19, 15, 9], [7, 20, 17, 18, 6, 22, 1, 23, 21, 3, 10, 4, 0, 5]]
            >>> print(data)
            [[ 2  8 24  5  3]
             [ 1 10 14 22 15]
             [ 4 21 19 23 25]
             [16 20 12 11 17]
             [13  6  9  7 18]]
            >>> print(_visualize_echelons(data.shape, result.peak_echelons, result.foundation_echelons))
            [[7 7 2 7 7]
             [7 7 7 1 6]
             [7 3 5 1 1]
             [6 3 7 7 6]
             [7 7 7 7 4]]

            >>> from echelon.test import _mock_2dim_data, _visualize_echelons
            >>> data, _ = _mock_2dim_data()
            >>> result = TwoDimEchelonAnalysis('8')(data)
            >>> result.peak_echelons
            [[14, 13], [2], [11, 16], [24]]
            >>> result.foundation_echelons
            [[8], [12], [19, 15, 9, 7, 20, 17, 18, 6, 22, 1, 23, 21, 3, 10, 4, 0, 5]]
            >>> print(data)
            [[ 2  8 24  5  3]
             [ 1 10 14 22 15]
             [ 4 21 19 23 25]
             [16 20 12 11 17]
             [13  6  9  7 18]]
            >>> print(_visualize_echelons(data.shape, result.peak_echelons, result.foundation_echelons))
            [[7 7 2 7 7]
             [7 7 7 5 7]
             [7 3 6 1 1]
             [7 3 7 7 7]
             [7 7 7 7 4]]
        """
        if self.adjacency_type == '4':
            W = self._canonical_twodim_adjacency_4(*data.shape)
        elif self.adjacency_type == '8':
            W = self._canonical_twodim_adjacency_8(*data.shape)

        return super().__call__(data.flatten(), W)


class DataFrameEchelonAnalysis(EchelonAnalysis):
    """The standard API for the data (realized values and neighborhood information) stored in a DataFrame."""
    def __call__(self, df,
                 value_colname: str,
                 id_colname: str,
                 adjacency_colname: str) -> Result_EchelonAnalysis:
        """
        Parameters:
            df (pd.DataFrame): the dataframe containing the indices, observed values, and adjacency information.
            value_colname: column name of ``df`` corresponding to the observed values.
            id_colname: column name of ``df`` corresponding to the index values. The values in this column needs to be unique.
            adjacency_colname: column name of ``df`` corresponding to the adjacency information. The cells must contain lists of indices to which the record is adjacent.
        """
        self.df = df
        self.id_colname = id_colname
        oracle = DataFrameEchelonOracle(df, value_colname, id_colname, adjacency_colname)
        return self._run_analysis(oracle)

    def echelon_hotspots(self, result: Result_EchelonAnalysis, total_count_colname, marked_count_colname):
        scan_oracle = DataFrameScanOracle(self.df, self.id_colname, total_count_colname, marked_count_colname)
        return super().echelon_hotspots(result, scan_oracle)
