from pyspark.sql.session import SparkSession
from .schema.Allowed_Amount.aa_pt_schema import AAPTSchema

class Guide:

    spark: SparkSession
    Writer: None
    Reader: None
    Schema: None

    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()
        self.AllowedAmount = AAPTSchema()
