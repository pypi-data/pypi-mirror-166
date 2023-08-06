from ..tbl.tbl_norms import TblNorms
from ..tbl.header_table import HeaderTable
from ..tbl.item_part_table import ItemPartTable
from .aa_header_table import AAHeaderTable
from .aa_item_table_out_of_network import AAItemTableOutOfNetwork
from .aa_item_table_allowed_amounts import AAItemTableAllowedAmounts
from .aa_item_table_out_of_network_payment import AAItemTableOutOfNetworkPayment


class AATBLNorms(TblNorms):
    header: HeaderTable = AAHeaderTable()
    items: {str: ItemPartTable} = {'out_of_network': AAItemTableOutOfNetwork,
                                   'allowed_amounts': AAItemTableAllowedAmounts,
                                   'out_of_network_payment': AAItemTableOutOfNetworkPayment}

    def __init__(self):
        super().__init__()
