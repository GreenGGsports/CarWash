from sqlalchemy import  Table, Column, Integer, ForeignKey
from src.models.base import BaseModel


reservation_extra = Table('reservation_extra', BaseModel.metadata,
    Column('reservation_id', Integer, ForeignKey('reservation.id'), primary_key=True),
    Column('extra_id', Integer, ForeignKey('Extra.id'), primary_key=True)
)