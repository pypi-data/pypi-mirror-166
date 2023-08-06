"""
Out of Network Payment Object table schema

https://github.com/CMSgov/price-transparency-guide/tree/bf0e394cf31813809d9b88f8fd7b002ccdfe9e5b/schemas/allowed-amounts#out-of-network-payment-object

"""


from ..tbl.item_part_table import ItemPartTable

from pyspark.sql.types import *
from pyspark.sql.types import StructType, StructField, FloatType, ArrayType

schema_provider = StructType([
    StructField("billed_charge", FloatType(), False),
    StructField("npi", ArrayType(StringType()), False)
])


class AAItemTableOutOfNetworkPayment(ItemPartTable):

    tbl_name = 'out_of_network_payment'

    schema: StructType = StructType([
        StructField("allowed_amount", FloatType(), False),
        StructField("billing_code_modifier", ArrayType(StringType()), True),
        StructField("providers", ArrayType(schema_provider), False)
    ])

    def __init__(self):
        # TODO: create standard on how to apply surrogate keys
        super().__init__()
