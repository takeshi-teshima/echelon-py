from copy import copy, deepcopy
import numpy as np
from echelon.oracle import EchelonOracleBase

## Type hinting
from typing import Tuple, List, Iterable
IndexType = int


def find_peak_echelons(oracle: EchelonOracleBase) -> List[List[IndexType]]:
    """
    Returns:
        peak_echelons

    Examples:
        >>> from .test import _mock_1dim_data
        >>> h, W = _mock_1dim_data()
        >>> from .oracle import NdarrayEchelonOracle
        >>> oracle = NdarrayEchelonOracle(h, W)
        >>> find_peak_echelons(oracle)
        [[16, 17, 15], [13], [6, 5, 7], [3], [23]]

    Notes:
        After finding the initial peaktop in each iteration,
        the algorithm takes the "set" of argmax indices,
        i.e., it considers the contour set in the neighborhood
        simultaneously as candidates.

            .. container:: algorithm-find-peaks
                :name: algorithm-find-peaks

                **Algorithm**

                #. We repeat the following until we run out of all unsearched indices.

                    #. Select one maximum point (summit, :math:`s`) and the max value (summit value, :math:`v`) among the unsearched indices. That is, :math:`s \in \mathrm{argmax}_{i \in \mathrm{unsearched}}\mathrm{Data}_i` and :math:`v = \mathrm{Data}_s`.
                    #. Initialize :math:`\mathrm{peak}=\{s\}`.
                    #. We now run the following extension loop:

                        We consider whether to extend :math:`\mathrm{peak}` to newly include
                        :math:`S := \mathrm{argmax}_{i \in N} \{\mathrm{Data}_i\}` where :math:`N := \mathrm{nb}(\mathrm{peak})`,
                        i.e., the maximizers among the neighbors of :math:`\mathrm{peak}`.
                        Here, argmax is understood as a set of indices.

                        * If :math:`S` contains no local minimum (i.e., if :math:`\mathrm{Data}_{i} \geq \max_{i \in \mathrm{nb}(N\cup S)}\mathrm{Data}_{i}` where :math:`i \in S`), then we extend the peak set: :math:`\mathrm{peak}\gets \mathrm{peak}\cup S`.
                        * Otherwise, we halt the extension loop, flag all elements of :math:`\mathrm{peak}` as searched, register :math:`\mathrm{peak}` as a found peak echelon, and go back to the top of the loop.

                #. After the loop is halted, we have the set of found :math:`\mathrm{peak}`'s (which may or may not jointly contain all indices. Those indices that do not belong to a peak echelon will belong to a foundation echelon later.).
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
        while _max > oracle.max_nb(_current_echelon + _argmax)[1]:
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


def _flatten_lists(lists: Iterable[list]) -> list:
    return sum(lists, [])


def find_foundation_echelons(oracle: EchelonOracleBase, peak_echelons: List[List[IndexType]]) -> List[List[IndexType]]:
    """Construct foundation echelons.

    Notes:
        The algorithm is as follows.
        In this algorithm, we keep track of the list of *families*.
        Each "family" is a set of indices, and the initial set of families consist of the peak echelons.
        In the latter steps, the set of families grow.

        We define :math:`\mathrm{TangentFamily}(\mathrm{indices}) := \{F \in \mathrm{families} : F \cap \mathrm{nb}(\mathrm{indices}) ≠ \emptyset\}`.
        We also define :math:`\mathrm{DataMax}(\mathrm{indices}) := \max_{i \in \mathrm{indices}}\mathrm{Data}_i`
        and :math:`\mathrm{DataArgMax}(\mathrm{indices}) := \mathrm{argmax}_{i \in \mathrm{indices}}\mathrm{Data}_i`

            .. container:: algorithm-find-foundations
                :name: algorithm-find-foundations

                **Algorithm**

                #. Mark all indices in Peak Echelons as searched.
                #. We repeat the following until we run out of all unsearched indices.

                    #. Select one maximum point (foundation-top, :math:`t`) and the max value (:math:`v`) among the unsearched indices. That is, :math:`t \in \mathrm{DataArgMax}(\mathrm{unsearched})` and :math:`v = \mathrm{DataMax}(\mathrm{unsearched})`.
                    #. Initialize :math:`\mathrm{foundation}=\{t\}`.
                    #. Initialize the set of families :math:`\mathrm{families} = \{\mathrm{peak}'s\}`.
                    #. Initialize the temporary family :math:`\mathrm{tempFamily} = \mathrm{foundation}`.
                    #. We now run the following extension loop, consisting of two steps: **family extension** and **neighbor extension**.

                        #. **Family extension**.

                           #. Pop out the set of tangent families:

                               * :math:`\mathcal{F} = \mathrm{TangentFamily}(\mathrm{tempFamily})`.
                               * :math:`\mathrm{families} \gets \mathrm{families} \setminus \mathcal{F}`.

                           #. Merge the tangent families as :math:`\mathrm{tempFamily} \gets \mathrm{tempFamily} \cup (\cup \mathcal{F})`.

                        #. **Neighbor extension**.
                           We decide whether to extend the set of families to neighbors.

                           #. Get the set of neighbors :math:`N := \mathrm{nb}(\mathrm{tempFamily})`.
                           #. Find :math:`A := \mathrm{DataArgMax}(N)`.

                               * If the maximum value :math:`\mathrm{Data}_i` (:math:`i \in A`) equals :math`v`, then we regard :math:`A` to be as qualified as :math:`t` to be part of :math:`\mathrm{foundation}`,
                                 and therefore

                                   * Add :math:`A` to the foundation: :math:`\mathrm{foundation} \gets \mathrm{foundation} \cup (A \cap \mathrm{unsearched})`.
                                   * Add :math:`A` to the temporary family: :math:`\mathrm{tempFamily} \gets \mathrm{tempFamily} \cup (A \cap \mathrm{unsearched})`.
                                   * Mark :math:`A` as searched.

                               * If elements of :math:`A` contains no local minima, i.e., if :math:`\mathrm{DataMax}(A\cup \mathrm{tempFamily}) \geq \mathrm{DataMax}(\mathrm{nb}(A\cup \mathrm{tempFamily}))`, then

                                   * Add :math:`A` to the foundation: :math:`\mathrm{foundation} \gets \mathrm{foundation} \cup (A \cap \mathrm{unsearched})`.
                                   * Add :math:`A` to the temporary family: :math:`\mathrm{tempFamily} \gets \mathrm{tempFamily} \cup (A \cap \mathrm{unsearched})`.
                                   * Mark :math:`A` as searched.

                               * Otherwise, we halt the iterative loop, register :math:`\mathrm{foundation}` as a foundation echelon, add :math:`\mathrm{tempFamily}` to the set :math:`\mathrm{families}` as an element, and go back to the top of the loop

                #. After the loop is halted, we have the set of found :math:`\mathrm{foundation}`'s.

                The set of foundation echelons and the set of peak echelons are mutually exclusive and collectively exhaustive.
    """
    unsearched_inds = list(set(oracle.copy_indices())-set(_flatten_lists(peak_echelons)))
    families = deepcopy(peak_echelons)
    foundation_echelons = []

    while len(unsearched_inds):
        _current_echelon = []
        ## Select a single point among the unsearched maxima.
        _argmax_single, _initial_max = oracle.find_peaktop(unsearched_inds)
        _argmax = [_argmax_single]
        _current_echelon += _argmax
        _current_family = _argmax

        while True:
            ## Blocking statement
            if (not oracle.nb(_current_family)) or (not unsearched_inds):
                break
            ## Family extension
            _current_family, families = oracle.pop_extend_family(_current_family, families)
            ## Check neighbor argmax set
            _argmax, _max = oracle.max_nb(_current_family)
            # If the max value is the same as the original max, unconditionally accept them.
            if (_max == _initial_max):
                _current_family += _argmax
                _current_echelon += _lists_intersection(_argmax, unsearched_inds) # Foundation echelon contains only those which do not consist the peak echelons.
            # If none of the neighboring candidates is a local minimum, accept the candidates.
            elif (_max > oracle.max_nb(_current_family + _argmax)[1]):
                _current_family += _argmax
                _current_echelon += _lists_intersection(_argmax, unsearched_inds) # Foundation echelon contains only those which do not consist the peak echelons.
            else:
                break

        families.append(_current_family)
        foundation_echelons.append(_current_echelon)
        unsearched_inds = list(set(unsearched_inds) - set(_current_echelon))
        if not unsearched_inds: # If all marked as searched
            break
    return foundation_echelons


def _lists_intersection(list1, list2) -> list:
    return list(set(list1).intersection(list2))


def find_echelon_clusters(peak_echelons, foundation_echelons, oracle):
    zones = deepcopy(peak_echelons)
    for echelon in foundation_echelons:
        for element in echelon:
            for i, zone in enumerate(zones):
                if _lists_intersection(oracle.nb([element]), zone):
                    zones[i].append(element)
    return zones
