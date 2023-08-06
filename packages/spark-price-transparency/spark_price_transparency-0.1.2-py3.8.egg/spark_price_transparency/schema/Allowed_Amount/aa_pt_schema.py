from ..pt_schema import PTSchema
from ..tbl.tbl_norms import TblNorms
from .aa_tbl_norms import AATBLNorms
from .aa_json_form import AAJSONForm


class AAPTSchema(PTSchema):

    tbl_norm: TblNorms = AATBLNorms
    json_form: AAJSONForm

    def __init__(self):
        """Allowed Amount PT Schema"""
        super().__init__()
