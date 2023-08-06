from datetime import date
from .orm_model import OrmModel
from .power_station import PowerStationShort

class Contract(OrmModel):
    id: int
    name: str
    date: date
    power_plant: PowerStationShort
    peak_power: float
    stage: str
    generated_power: float
    tn_co2_avoided: float
    eq_family_consumption: float
    sent_state: str
    product_mode: str
    payment_period: str
    investment: float
    bank_account: str