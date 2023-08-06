from .orm_model import OrmModel
from pydantic import EmailStr, Field, validator
from typing import List, Optional
from .info import PersonType, State, Country
from .bank_account import BankAccountOut

class UserIn(OrmModel):
    person_type:    Optional[int]= Field(alias='person_type_id')
    firstname:      Optional[str]
    lastname:       Optional[str]
    street:         Optional[str]
    street2:        Optional[str] = Field(alias='additional_street')
    zip:            Optional[str]
    city:           Optional[str]
    state_id:       Optional[int]
    country_id:     Optional[int]
    email:          Optional[EmailStr]
    phone:          Optional[str]
    alias:          Optional[str]
    vat:            Optional[str]
    gender_partner: Optional[str] = Field(alias='gender')
    birthday:       Optional[str]

class UserOut(OrmModel):
    id:                int
    person_type:       PersonType
    firstname:         str
    lastname:          str
    street:            str
    additional_street: Optional[str] = Field(alias='street2')
    zip:               str
    city:              str
    state:             State = Field(alias='state_id')
    country:           Country = Field(alias='country_id')
    email:             EmailStr
    phone:             str
    alias:             str
    vat:               str
    gender:            Optional[str] = Field(alias='gender_partner')
    birthday:          str
    bank_accounts:     List[BankAccountOut] = Field(alias='bank_ids')
