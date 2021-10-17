from copy import copy
import numpy as np

## Typing
from typing import Tuple, Any, List
IndexType = int
import numpy as np


def _lists_intersection(list1, list2) -> list:
    return list(set(list1).intersection(list2))


def _mock_pytest_data():
    n = 5
    v = np.array([5, 3, 2, 5, 4])
    w = np.zeros((n, n))
    w[np.eye(len(w), k=1, dtype='bool')] = 1
    w[np.eye(len(w), k=-1, dtype='bool')] = 1
    oracle = NdarrayEchelonOracle(v, w)
    return v, w


class EchelonOracleBase:
    def __init__(self, max_of_empty:Any=-np.inf):
        """
        Parameters:
            max_of_empty: value to return if the indices list is empty.
        """
        self.max_of_empty = max_of_empty

    def copy_indices(self) -> List[IndexType]:
        """Return a copy of the set of all indices (copy thus mutation is allowed)."""
        pass

    def nb(self, indices: List[IndexType]) -> List[IndexType]:
        """Find neighboring indices (excluding the input indices themselves)."""
        pass

    def max_indices(self, indices: List[IndexType]) -> Tuple[List[IndexType], Any]:
        """Find the maximum and argmax of the data among the input indices.

        Parameters:
            indices: indices to query.
        """
        pass

    def find_peaktop(self, indices: List[IndexType]) -> Tuple[IndexType, Any]:
        """
        Examples:
            >>> NdarrayEchelonOracle(*_mock_pytest_data()).find_peaktop([1, 2, 3])
            (3, 5)
        """
        _argmax_list, _max = self.max_indices(indices)
        return _argmax_list[0], _max

    def max_nb(self, indices: List[IndexType]) -> Tuple[List[IndexType], Any]:
        """
        Examples:
            >>> NdarrayEchelonOracle(*_mock_pytest_data()).max_nb([1, 2])
            ([0, 3], 5)
        """
        nb_indices = self.nb(indices)
        return self.max_indices(nb_indices)

    def max_nb_indices(self, ind1, ind2):
        inds = _lists_intersection(self.nb(ind1), ind2)
        return self.max_indices(inds)

    def pop_extend_family(self, indices, families):
        _family_i = copy(indices)
        _del_families = []
        for i, family in enumerate(families):
            if _lists_intersection(self.nb(indices), family):
                _family_i += family
                _del_families.append(i)
        if _del_families:
            families = np.delete(families, _del_families).tolist()
        return _family_i, families


class NdarrayEchelonOracle(EchelonOracleBase):
    def __init__(self, values: np.ndarray, adjacency: np.ndarray):
        """
        Parameters:
            data: 1-dimensional array of the observed values for the grids.
            adjacency: 2-dimensional adjacency matrix for the grids.
        """
        super().__init__()
        assert len(values) == len(adjacency)
        self.values = values
        self.adjacency = adjacency

    def copy_indices(self) -> List[IndexType]:
        return list(range(len(self.values)))

    def nb(self, indices: List[IndexType]) -> List[IndexType]:
        """
        Examples:
            >>> NdarrayEchelonOracle(*_mock_pytest_data()).nb([1, 2])
            [0, 3]
        """
        _adj = self.adjacency[indices]
        _adj = np.logical_or.reduce(_adj)
        _neighbors = list(np.nonzero(_adj)[0])
        return list(set(_neighbors)-set(indices))

    def max_indices(self, indices: List[IndexType]) -> Tuple[List[IndexType], Any]:
        """
        Examples:
            >>> NdarrayEchelonOracle(*_mock_pytest_data()).max_indices([1, 2])
            ([1], 3)
        """
        if not indices:
            return [], self.max_of_empty

        vals = self.values[indices]
        _max = np.max(vals)
        _argmax_list = [indices[i] for i in np.flatnonzero(vals == _max)]
        return _argmax_list, _max
