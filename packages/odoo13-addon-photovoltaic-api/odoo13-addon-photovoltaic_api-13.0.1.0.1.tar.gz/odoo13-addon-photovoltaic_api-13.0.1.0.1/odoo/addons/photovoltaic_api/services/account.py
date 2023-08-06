from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.exceptions import AccessError, MissingError, UserError
import secrets
from datetime import datetime, timedelta


class AccountService(Component):
    _inherit = 'base.rest.service'
    _name = 'account.service'
    _usage = 'account'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/signup_request'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_signup_request'),
    )
    def signup_request(self, **params):
        '''
        Request to create a user from a partner
        :param vat: VAT
        :return: Signup token
        '''
        partner = self.env['res.partner'].search([('vat', '=', params.get('vat'))])
        if len(partner) < 1:
            raise MissingError('Missing error')
        elif len(partner) > 1:
            raise UserError('Bad request')

        expiration = datetime.now() + timedelta(hours=1)
        partner.signup_prepare(expiration=expiration)
        return {
            'token': partner.signup_token,
            'email': partner.email,
            'name':  partner.name
        }

    @restapi.method(
        [(['/signup'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_signup'),
    )
    def signup(self, **params):
        '''
        Confirm signup with a signup token
        :param token: Signup token from signup_request
        :param password: Password
        :return: {VAT, API Key}
        '''
        token = params.get('token')
        password = params.get('password')

        partner = self.env['res.partner'].search([('signup_token', '=', token)])

        if len(partner) != 1:
            raise MissingError('Missing error')

        self.env['res.users'].signup({
            'login': partner.vat,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            'password': password
        }, token)

        user = self.env['res.users'].search([('login', '=', partner.vat)])
        secret = secrets.token_hex()

        api_key = self.env['auth.api.key'].search([('user_id', '=', user.id)])
        if len(api_key) == 1:
            api_key.write({'key': secret})
        else:
            self.env['auth.api.key'].create({
                'name': partner.vat,
                'user_id': user.id,
                'key': secret
            })

        return {
            'login': partner.vat,
            'api_key': secret,
            'email': partner.email,
            'name':  partner.name
        }

    @restapi.method(
        [(['/login'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_login'),
    )
    def login(self, **params):
        '''
        Get API Key with login credentials
        :param vat: VAT
        :param password: Password
        :return: API Key
        '''
        user = self.env['res.users'].authenticate(
            '',
            params.get('vat'),
            params.get('password'),
            {'interactive': False})

        return self.env['auth.api.key'].search([('user_id', '=', user)]).key

    # Private methods
    def _validator_signup_request(self):
        return {
            'vat':      {'type': 'string'}
        }

    def _validator_signup(self):
        return {
            'token':    {'type': 'string'},
            'password': {'type': 'string'}
        }

    def _validator_login(self):
        return {
            'vat':      {'type': 'string'},
            'password': {'type': 'string'}
        }