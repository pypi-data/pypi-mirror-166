from pyspark.sql import DataFrame


class PTSchema:
    """Report Base Class is to contain all data elements related to report regulation"""
    tbl_norm: None  # TODO: Create Norm class which is a header + Normalized Tables
    json_form: None  # TODO: Create JSON Form class which has a json_header + json_item
    df: {str: DataFrame}

    def __init__(self, src_type: str = "db", src_path: str = None):
        self.src_type = src_type
        self.src_path = src_path

    def set_header(self) -> DataFrame:
        """Set self.df['header'] and return DataFrame of just the header record"""
        pass

    def set_item(self) -> DataFrame:
        """Set self.df['item'] and return complex struct DataFrame of item records"""
        pass

    def read_tbl_norms(self) -> {str: DataFrame}:
        """Return dict of tables (derived from read_item)"""
        pass

    def ingest(self) -> None:
        """Read the contents of a directory and ingest into target delta tables"""
        pass

    def write_json_report(self, tgt_folder) -> None:
        pass
