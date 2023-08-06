import random

from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class OrderModel(BaseModel):

    """  Наряды """

    __tablename__ = 'orders'
    __table_args__ = {"extend_existing": True}

    user_uuid = Column(UUID)
    status = Column(String, default='created', nullable=False)
    description = Column(String)

    service_requests_id = Column(Integer, ForeignKey('service_requests.id'))
    service_requests = relationship('ServiceRequests', back_populates='orders', uselist=False)
