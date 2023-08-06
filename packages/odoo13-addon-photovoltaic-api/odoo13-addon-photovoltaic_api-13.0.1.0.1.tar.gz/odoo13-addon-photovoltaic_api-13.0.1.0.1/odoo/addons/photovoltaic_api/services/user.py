from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

from ..pydantic_models.bank_account import BankAccountOut
from ..pydantic_models.info import Country, PersonType, State
from ..pydantic_models.user import UserIn, UserOut


class UserService(Component):
    _inherit = 'base.rest.service'
    _name = 'user.service'
    _usage = 'user'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/'], 'GET')],
        output_param=restapi.PydanticModel(UserOut)
    )
    def get(self):
        return UserOut.from_orm(self.env.user.partner_id)

    @restapi.method(
        [(['/'], 'PUT')],
        input_param=restapi.PydanticModel(UserIn),
        output_param=restapi.PydanticModel(UserOut)
    )
    def update(self, user_in):
        partner = self.env.user.partner_id
        partner.write(user_in.dict(exclude_unset=True))

        user = self.env['res.users'].search([('partner_id', '=', partner.id)])
        user.sudo().write({'login': partner.vat})

        api_key = self.env['auth.api.key'].sudo().search([('user_id', '=', user.id)])
        api_key.sudo().write({'name': partner.vat})

        return UserOut.from_orm(partner)
