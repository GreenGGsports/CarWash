from sqlalchemy import Table, Column, Integer, ForeignKey
from src.models.base import BaseModel

service_extra = Table(
    'service_extra', BaseModel.metadata,
    Column('service_id', Integer, ForeignKey('Service.id')),
    Column('extra_id', Integer, ForeignKey('Extra.id'))
)
