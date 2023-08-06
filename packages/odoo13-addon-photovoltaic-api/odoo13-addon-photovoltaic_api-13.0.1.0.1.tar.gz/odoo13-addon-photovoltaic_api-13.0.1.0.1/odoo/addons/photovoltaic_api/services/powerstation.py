from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.exceptions import AccessError, MissingError

from ..pydantic_models.power_station import PowerStation


class PowerStationService(Component):
    _inherit = 'base.rest.service'
    _name = 'powerstation.service'
    _usage = 'powerstation'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/<int:_id>'], 'GET')],
        output_param=restapi.PydanticModel(PowerStation)
    )
    def get(self, _id):
        station = self.env['photovoltaic.power.station'].browse(_id)
        try:
            return PowerStation.from_orm(station)

        except AccessError:
            # Return 404 even if it is from a different user
            # to not leak information
            raise MissingError('Access error')


    # Private methods
    def _to_json(self, station):
        return {
            'id': station.id,
            'name': station.name,
            'image': station.image,
            'province': station.province,
            'link_google_maps': station.link_google_maps,
            'peak_power': station.peak_power,
            'rated_power': station.rated_power,
            'start_date': station.start_date,
            'monit_link': station.monit_link,
            'monit_user': station.monit_user,
            'monit_pass': station.monit_pass,
            'tecnical_memory_link': station.tecnical_memory_link,
            'annual_report_link': station.annual_report_link,
            'energy_generated': station.energy_generated,
            'co2': station.co2,
            'reservation': station.reservation,
            'contracts_count': station.contracts_count,
            # 'eq_family_consumption',
        }
