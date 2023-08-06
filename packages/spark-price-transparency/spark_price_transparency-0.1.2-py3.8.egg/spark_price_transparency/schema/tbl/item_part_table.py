from delta import DeltaTable
from delta.tables import DeltaTableBuilder
from pyspark.sql import SparkSession, DataFrame, types as T, functions as F
from math import floor
import dbldatagen as dg

class ItemPartTable:

    db_name: str
    tbl_name: str
    name: str
    schema: T.StructType

    def __init__(self, db_name='pt', tbl_name=None):
        self.db_name = db_name
        self.tbl_name = tbl_name
        self.name = f"{self.db_name}.{self.tbl_name}"

    def create_table(self, spark: SparkSession = None) -> DeltaTable:
        """
        CREATES Item Part Table in the MetaStore
        :return: Delta Table
        """
        spark = SparkSession.getActiveSession() if spark is None else spark
        dtc: DeltaTableBuilder = DeltaTable.createIfNotExists(spark).tableName(self.name)
        for fld in self.schema.fields:
            dtc.addColumn(colName=fld.name,
                          dataType=fld.dataType,
                          comment="")
        return dtc.execute()
