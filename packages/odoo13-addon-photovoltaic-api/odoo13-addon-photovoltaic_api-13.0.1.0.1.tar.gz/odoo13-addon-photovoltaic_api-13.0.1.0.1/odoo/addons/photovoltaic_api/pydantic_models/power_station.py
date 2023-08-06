from datetime import date

from pydantic import BaseModel, Field

from .orm_model import OrmModel


class PowerStation(OrmModel):
    id: int
    name: str
    display_name: str = Field(alias='name_display')
    image: str
    province: str
    link_google_maps: str
    peak_power: str
    rated_power: str
    start_date: date
    monit_link: str
    monit_user: str
    monit_pass: str
    tecnical_memory_link: str
    annual_report_link: str
    energy_generated: str
    tn_co2_avoided: str = Field(alias='co2')
    reservation: float
    contracts_count: int

class PowerStationShort(BaseModel):
    id: int
    name: str
    display_name: str
