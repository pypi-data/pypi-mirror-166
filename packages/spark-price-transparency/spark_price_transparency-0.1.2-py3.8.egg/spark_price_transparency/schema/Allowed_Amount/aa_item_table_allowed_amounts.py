"""
Allowed Amount table schema
https://github.com/CMSgov/price-transparency-guide/tree/bf0e394cf31813809d9b88f8fd7b002ccdfe9e5b/schemas/allowed-amounts#allowed-amounts-object

"""
from ..tbl.item_part_table import ItemPartTable
from .aa_item_table_tax_identifier import AAItemTableTaxIdentifier
from .aa_item_table_out_of_network_payment import AAItemTableOutOfNetworkPayment
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

schema_tin = AAItemTableTaxIdentifier.schema
schema_oon_payment = AAItemTableOutOfNetworkPayment.schema


class AAItemTableAllowedAmounts(ItemPartTable):

    tbl_name = 'allowed_amounts'

    schema = StructType([
        StructField("tin", schema_tin, False),
        StructField("service_code", ArrayType(StringType()), True),
        StructField("billing_class", StringType(), False),
        StructField("payments", ArrayType(schema_oon_payment), False)
    ])

    def __init__(self):
        super().__init__()
