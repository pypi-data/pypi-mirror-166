from .orm_model import OrmModel

class Allocation(OrmModel):
    id: int
    amount: int
    period: int
    year: int
    state: str
    energy_generated: float
    tn_co2_avoided: float
    eq_family_consumption: float
    type: str