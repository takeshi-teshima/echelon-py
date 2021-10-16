import numpy as np
IndexType = int

from .oracle import EchelonOracleBase

## Type hinting
from typing import Tuple, List, Iterable

def _lists_intersection(list1, list2) -> list:
    return list(set(list1).intersection(list2))

def _reduce_lists(lists: Iterable[list]) -> list:
    return sum(lists, [])

def _mock_1dim_data():
    h = np.array([1, 2, 3, 4, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 1])
    W = np.zeros((25, 25), dtype='int8')
    W[np.eye(len(W), k=1, dtype='bool')] = 1
    W[np.eye(len(W), k=-1, dtype='bool')] = 1
    return h, W


def find_peak_echelons(oracle: EchelonOracleBase) -> List[List[IndexType]]:
    """
    Returns:
        peak_echelons

    Examples:
        >>>h, W = _mock_1dim_data()
        >>>oracle = NdarrayEchelonOracle(h, W)
        >>>find_peak_echelons(oracle)
        [[16, 17, 15], [13], [6, 5, 7], [3], [23]]

    Notes:
        After finding the initial peaktop in each iteration,
        the algorithm takes the "set" of argmax indices,
        i.e., it considers the contour set in the neighborhood
        simultaneously as candidates.
    """
    indices = oracle.copy_indices()
    peak_echelons = []
    while len(indices):
        _current_echelon = []
        _removed = []

        ## Start from finding a single peak point among the remaining candidates.
        _argmax_single, _max = oracle.find_peaktop(indices)
        _argmax = [_argmax_single]

        ## Extend from the peak point to its neighbors until the search hits a local minimum.
        ## Handle ties simultaneously (i.e., argmax is a set, not a point).
        while _max >= oracle.max_nb(_current_echelon + _argmax)[1]:
            ## If not local minimum, add to peak echelon
            ## and remove searched candidates.
            _current_echelon += _argmax
            _removed += _argmax
            ## And continue to next round
            _argmax, _max = oracle.max_nb(_current_echelon)
        _removed += _argmax # Remove searched candidates
        if len(_current_echelon):
            peak_echelons.append(_current_echelon)
        indices = list(set(indices) - set(_current_echelon) - set(_removed))
    return peak_echelons


from copy import deepcopy
def find_foundation_echelons(oracle: EchelonOracleBase, peak_echelons: List[List[IndexType]]) -> List[List[IndexType]]:
    unsearched_inds = list(set(oracle.copy_indices())-set(_reduce_lists(peak_echelons)))
    families = deepcopy(peak_echelons)
    foundation_echelons = []

    while len(unsearched_inds):
        _current_echelon = []
        ## Select a single point among the unsearched maxima.
        _argmax_single, _initial_max = oracle.find_peaktop(unsearched_inds)
        _argmax = [_argmax_single]
        _current_echelon += _argmax
        _current_family = _argmax
        unsearched_inds = list(set(unsearched_inds) - set(_argmax))

        while True:
            ## Blocking statement
            if (not oracle.nb(_current_family)) or (not unsearched_inds):
                break
            ## Extend to family
            _current_family, families = oracle.pop_extend_family(_current_family, families)
            ## Check neighbor argmax set
            _argmax, _max = oracle.max_nb(_current_family)
            # If the max value is the same as the original max, unconditionally accept them.
            if (_max == _initial_max):
                _current_family += _argmax
                _current_echelon += _argmax # Foundation echelon contains only those which do not consist the peak echelons.
                unsearched_inds = list(set(unsearched_inds) - set(_argmax))
            # If none of the neighboring candidates is a local minimum, accept the candidates.
            elif (_max > oracle.max_nb(_current_family + _argmax)[1]):
                _current_family += _argmax
                _current_echelon += _argmax # Foundation echelon contains only those which do not consist the peak echelons.
                unsearched_inds = list(set(unsearched_inds) - set(_argmax))
            else:
                break

        families.append(_current_family)
        foundation_echelons.append(_current_echelon)
        if not unsearched_inds: # If all marked as searched
            break
    return foundation_echelons


from copy import copy
def find_echelon_clusters(peak_echelons, foundation_echelons, oracle):
    zones = copy(peak_echelons)
    for echelon in foundation_echelons:
        for element in echelon:
            for i, zone in enumerate(zones):
                if _lists_intersection(oracle.nb([element]), zone):
                    zones[i].append(element)
    return zones
