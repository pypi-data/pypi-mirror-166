import random

from sqlalchemy import (Column, Integer, String, ForeignKey, Computed, Boolean)
from sqlalchemy.dialects.postgresql import JSONB, UUID, TSVECTOR
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .resources.sql_requests import SqlRequests


class ServiceRequests(BaseModel):

    """  Заявки """

    __tablename__ = 'service_requests'
    __table_args__ = {"extend_existing": True}

    request_number = Column(Integer, nullable=False, default=random.randint(1, 10_000))
    status = Column(String, default='created', nullable=False)
    user_uuid = Column(UUID)
    service_model_data = Column(JSONB)
    responsible = Column(String, default="resident")
    description = Column(String)
    is_manager = Column(Boolean, default=False)

    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartments.id'), nullable=True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=True)

    service = relationship('Services', back_populates='service_requests', uselist=False)
    apartment = relationship('Apartments', uselist=False)
    public_space = relationship('Buildings', uselist=False)
    files = relationship('NextcloudFiles', back_populates='service_requests', uselist=True)
    orders = relationship('OrderModel', back_populates='service_requests', uselist=True)

    ts_vector = Column(TSVECTOR, Computed(SqlRequests.transformation_to_ts_vector(),  persisted=True))
