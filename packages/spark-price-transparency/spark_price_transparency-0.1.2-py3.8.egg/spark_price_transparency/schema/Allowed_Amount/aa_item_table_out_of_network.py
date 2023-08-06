"""
Out Of Network Object table schema
https://github.com/CMSgov/price-transparency-guide/tree/bf0e394cf31813809d9b88f8fd7b002ccdfe9e5b/schemas/allowed-amounts#out-of-network-object

"""

from ..tbl.item_part_table import *
from .aa_item_table_allowed_amounts import AAItemTableAllowedAmounts

schema_allowed_amount = AAItemTableAllowedAmounts.schema

class AAItemTableOutOfNetwork(ItemPartTable):
    tbl_name = 'out_of_network'

    schema = T.StructType([
        T.StructField("name", T.StringType(), False),
        T.StructField("billing_code_type", T.StringType(), False),
        T.StructField("billing_code", T.StringType(), False),
        T.StructField("billing_code_type_version", T.StringType(), False),
        T.StructField("description", T.StringType(), False),
        T.StructField("allowed_amounts", T.ArrayType(schema_allowed_amount), False)
    ])

    def __init__(self):
        super().__init__()

    @staticmethod
    def gen_df(aa_header_keys: DataFrame,
               num_oon=2,
               recs_per_partition=5.0) -> DataFrame:
        # TODO: Add Billing Code Types to reference table and pull possible values from there
        head_num = aa_header_keys.count()
        num_rec = head_num * num_oon
        return aa_header_keys \
            .join(dg.DataGenerator(sparkSession=SparkSession.getActiveSession(),
                                   name="gen_aa_oon",
                                   rows=num_rec,
                                   startingId=0,
                                   randomSeed=6875309,
                                   partitions=floor(num_rec / recs_per_partition))
                  .withColumn("oon_id", T.LongType(), expr='id')
                  .withColumn("name", T.StringType(), expr=f'CONCAT("name_", CAST(2000000000 + id AS STRING))')
                  .withColumn("billing_code_type", T.StringType(),
                              values=['CPT', 'NDC', 'HCPCS', 'RC', 'ICD', 'MS-DRG', 'R-DRG', 'S-DRG',
                                      'APS-DRG', 'AP-DRG', 'APR-DRG', 'APC', 'LOCAL', 'EAPG', 'HIPPS', 'CDT'],
                              random=True)
                  .withColumn("billing_code", T.StringType(), minValue=100, maxValue=999, random=True)
                  .withColumn("description", T.StringType(),
                              expr=f'CONCAT("desc_", CAST(2000000000 + id AS STRING))').build()
                  .withColumn("billing_code", F.concat(F.lit('B'), F.substring(F.col('billing_code'), 1, 2),
                                                       F.lit('.'), F.substring(F.col('billing_code'), 3, 1))),
                  F.col('head_id') == F.col('oon_id'), 'left')
