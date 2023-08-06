from pydantic import BaseModel
from odoo.addons.pydantic import utils

class OrmModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter
