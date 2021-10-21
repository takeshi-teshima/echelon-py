import numpy as np

# Type hinting
from typing import List, Tuple, Any
from abc import ABCMeta, abstractmethod


class EchelonScanStop(Exception):
    pass


class ScanOracleBase(metaclass=ABCMeta):
    @abstractmethod
    def score(self, indices: List[int]) -> Tuple[Any, dict]:
        pass


class ApproxBinomialScanOracleBase(ScanOracleBase):
    """
    Notes:
        Consider :math:`K` regions and let us denote :math:`[K] := \{1, 2, \ldots, K\}`.
        For each region :math:`k \in [K]`, assume :math:`c_k \sim \mathrm{Bi}(\theta_k, n_k)`.

        Consider a region :math:`Z \subset [K]`. We assign a score :math:`s` that indicates how "hot-spot-ish" the region :math:`Z` is.

        Let us assume that :math:`(\theta_k)_{k\in Z}` and :math:`(\theta_k)_{k\in Z^\mathrm{c}}` are constants, :math:`\theta_Z` and :math:`\theta_{Z^\mathrm{c}}`, respectively.
        We compare the maximum likelihood under :math:`\theta_Z = \theta_{Z^\mathrm{c}}` and :math:`\theta_Z > \theta_{Z^\mathrm{c}}`.
        Denote :math:`c_Z := \sum_{k \in Z} c_k`, :math:`n_Z := \sum_{k \in Z} n_k`, :math:`n_{Z^{\mathrm{c}}} := \sum_{k \in Z^{\mathrm{c}}} n_k`, and :math:`n_{Z^{\mathrm{c}}} := \sum_{k \in Z^{\mathrm{c}}} n_k`.

        Now, by the reproductive property, :math:`c_Z \sim \mathrm{Bi}(\theta_Z, n_Z)` where :math:`\theta_Z = \sum_{k \in Z} \theta_k`.
        Similarly for :math:`c_{Z^\mathrm{c}}`.
        Since the maximum likelihood of :math:`c \sim \mathrm{Bi}(\theta, n)` is :math:`\mathrm{Bi}(\frac{c}{n}, n)(c)` (by abuse of notation, we denote the density of a distribution by the name of the distribution).

        Now, when :math:`n >> c`, we have :math:`\mathrm{Bi}(\theta, n)(c) \simeq (\theta)^c`.

        With this approximation, the score for the case that :math:`\theta_Z > \theta_{Z^\mathrm{c}}` is
        :math:`\log (\frac{c_Z}{n_Z})^{c_Z} + \log (\frac{c_{Z^\mathrm{c}}}{n_{Z^\mathrm{c}}})^{c_{Z^\mathrm{c}}}`.

        Similarly, the score for the case that :math:`\theta_Z = \theta_{Z^\mathrm{c}}` is :math:`\log (\frac{c_{[K]}}{n_{[K]}})^{c_{[K]}}`.

        Thus, we use
        :math:`\log (\frac{c_Z}{n_Z})^{c_Z} + \log (\frac{c_{Z^\mathrm{c}}}{n_{Z^\mathrm{c}}})^{c_{Z^\mathrm{c}}} - \log (\frac{c_{[K]}}{n_{[K]}})^{c_{[K]}}`
        as the score.
    """
    def __init__(self, all_total_count, all_marked_count):
        self._all_total_count = all_total_count
        self._all_marked_count = all_marked_count

    @property
    def all_total_count(self):
        return self._all_total_count

    @property
    def all_marked_count(self):
        return self._all_marked_count

    def score(self, Z):
        nG = self.all_total_count
        cG = self.all_marked_count
        nZ = self.total_count(Z)
        cZ = self.marked_count(Z)
        ## Stopping criterion
        if nZ >= nG * .5:
            raise EchelonScanStop()
        nZc = nG - nZ
        cZc = cG - cZ
        ## Scores
        score = (cZ * (np.log(cZ) - np.log(nZ)) + cZc * (np.log(cZc) - np.log(nZc))) * ((cZ/nZ > cZc/nZc) * 1.)
        log_lambda = score - cG * np.log(cG / nG) * ((cZ/nZ > cZc/nZc) * 1.)
        return log_lambda, {'c(Z)': cZ,
                            #'raw_score': score, # score may be too small in typical use cases, and hence may be confusing.
                            'log_lambda': log_lambda}

    @abstractmethod
    def total_count(self, indices):
        pass

    @abstractmethod
    def marked_count(self, indices):
        pass


class NdarrayScanOracle(ApproxBinomialScanOracleBase):
    def __init__(self, total_count: np.ndarray, marked_count: np.ndarray):
        super().__init__(total_count.sum(), marked_count.sum())
        self.total_count_data = total_count.flatten()
        self.marked_count_data = marked_count.flatten()

    def total_count(self, indices: List[int]):
        return self.total_count_data[indices].sum()

    def marked_count(self, indices: List[int]):
        return self.marked_count_data[indices].sum()


class DataFrameScanOracle(ScanOracleBase):
    def __init__(self, df, id_colname: str, total_count_col: str, marked_count_col: str):
        self.df = df
        self.id_colname = id_colname
        self.total_count_col = total_count_col
        self.marked_count_col = marked_count_col

    def _subset(self, indices):
        return self.df[self.df[self.id_colname].isin(indices)]

    def total_count(self, indices):
        return self._subset(indices)[self.total_count_col].sum()

    def marked_count(self, indices):
        return self._subset(indices)[self.marked_count_col].sum()
