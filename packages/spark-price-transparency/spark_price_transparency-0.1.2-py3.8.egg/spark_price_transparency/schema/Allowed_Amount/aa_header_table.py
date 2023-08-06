from ..tbl.header_table import *
from .aa_item_table_out_of_network import AAItemTableOutOfNetwork

schema_oon = AAItemTableOutOfNetwork.schema

class AAHeaderTable(HeaderTable):
    tbl_name = "allowed_amounts_report"

    schema = T.StructType([
        T.StructField("reporting_entity_name", T.StringType(), False, {'comment': "PARTITION KEY"}),
        T.StructField("reporting_entity_type", T.StringType(), False),
        T.StructField("plan_name", T.StringType(), True),
        T.StructField("plan_id_type", T.StringType(), True),
        T.StructField("plan_id", T.StringType(), True, {'comment': "KEY"}),
        T.StructField("plan_market_type", T.StringType(), True),
        T.StructField("out_of_network", T.ArrayType(schema_oon), False, {'comment': "NESTED ELEMENT"}),
        T.StructField("last_updated_on", T.DateType(), False, {'comment': "PARTITION KEY"}),
        T.StructField("version", T.StringType(), False)
    ])

    def __init__(self):
        super().__init__()

    @staticmethod
    def gen_df(num_entity=2,
               num_plan_id=3,
               recs_per_partition=5.0) -> DataFrame:
        return dg.DataGenerator(sparkSession=SparkSession.getActiveSession(),
                                name="gen_aa_header",
                                rows=num_entity * num_plan_id,
                                startingId=0,
                                randomSeed=42,
                                partitions=floor(num_entity * num_plan_id / recs_per_partition)) \
            .withColumn("aa_header_id", expr='id') \
            .withColumn("reporting_entity_name", T.StringType(),
                        expr=f'CONCAT("entity_", CAST(1000000000 + FLOOR(id/{num_plan_id}) AS STRING))') \
            .withColumn("reporting_entity_type", T.StringType(),
                        values=['group health plan', 'health insurance issuer', 'third party'],
                        random=True, weights=[5, 3, 2]) \
            .withColumn("plan_name", T.StringType(), values=['', ]) \
            .withColumn("plan_id_type", T.StringType(), values=["EIN", "HIOS"], random=True, weights=[1, 1]) \
            .withColumn("plan_id", T.StringType(), expr=f'CAST(MOD(id, {num_plan_id}) AS STRING)') \
            .withColumn("plan_market_type", T.StringType(), values=["group", "individual"], random=True) \
            .withColumn("last_updated_on", T.DateType(), expr='DATE(NOW())') \
            .build() \
            .withColumn("plan_id", F.when(F.col("plan_id_type") == F.lit("EIN"), F.lpad(F.col("plan_id"), 9, "0"))
                        .otherwise(F.lpad(F.col("plan_id"), 10, "0"))) \
            .withColumn("plan_name", F.concat(F.lit('plan_'), F.col('plan_id')))
