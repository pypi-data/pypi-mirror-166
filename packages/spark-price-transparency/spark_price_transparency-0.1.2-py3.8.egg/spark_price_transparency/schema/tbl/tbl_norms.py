import pyspark
from .header_table import HeaderTable
from .item_part_table import ItemPartTable


class TblNorms:
    """Tbl_Norms class is the collection of Header_Table + Item_Part_Tables"""

    header: HeaderTable
    items: {str: ItemPartTable}

    def __init__(self):
        """When initializing Tbl norms need ot create complete class of header+items"""
        self.x = 110
