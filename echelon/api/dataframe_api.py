from echelon.api.base import EchelonAnalysis
from echelon.oracle import DataFrameEchelonOracle
from echelon.scan_oracle import DataFrameScanOracle

# Type hinting
from echelon.api.base import Result_EchelonAnalysis

class DataFrameEchelonAnalysis(EchelonAnalysis):
    """The standard API for the data (realized values and neighborhood information) stored in a DataFrame."""
    def echelon_hotspots(self, result: Result_EchelonAnalysis, total_count_colname, marked_count_colname):
        scan_oracle = DataFrameScanOracle(self.df, self.id_colname, total_count_colname, marked_count_colname)
        return super().echelon_hotspots(result, scan_oracle)

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
