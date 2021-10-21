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
