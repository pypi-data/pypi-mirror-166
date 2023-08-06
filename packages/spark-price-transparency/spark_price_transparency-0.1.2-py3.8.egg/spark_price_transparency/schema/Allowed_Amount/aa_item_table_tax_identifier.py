"""
Tax Identifier Object table schema
https://github.com/CMSgov/price-transparency-guide/tree/bf0e394cf31813809d9b88f8fd7b002ccdfe9e5b/schemas/allowed-amounts#tax-identifier-object

"""
from ..tbl.item_part_table import ItemPartTable
from pyspark.sql.types import StructType, StructField, StringType


class AAItemTableTaxIdentifier(ItemPartTable):

    tbl_name = 'tax_identifier'

    schema = StructType([
        StructField("type", StringType(), False),
        StructField("value", StringType(), False)
    ])

    def __init__(self):
        super().__init__()
