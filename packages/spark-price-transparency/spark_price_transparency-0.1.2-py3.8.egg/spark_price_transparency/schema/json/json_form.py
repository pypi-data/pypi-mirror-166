from .header_json import HeaderJSON
from .item_json import ItemJSON


class JSONForm:

    header: HeaderJSON
    items: {str: ItemJSON}

    def __init__(self):
        """When initializing json form, we need both the header and the item"""
        self.x = 110
