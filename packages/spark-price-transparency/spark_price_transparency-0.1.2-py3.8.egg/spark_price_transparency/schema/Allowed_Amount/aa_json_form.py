from ..json.json_form import JSONForm
from ..json.header_json import HeaderJSON
from .aa_header_json import AAHeaderJSON
from ..json.item_json import ItemJSON
from .aa_item_json_out_of_network import AAItemJSONOutOfNetwork


class AAJSONForm(JSONForm):

    header: HeaderJSON = AAHeaderJSON
    items: {str: ItemJSON} = {'out_of_network': AAItemJSONOutOfNetwork}

    def __init__(self):
        super().__init__()
