from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class ServiceCategories(BaseModel):

    """  Справочник категорий услуг"""

    __tablename__ = 'service_categories'
    __table_args__ = {"extend_existing": True}

    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    parent_category_id = Column(Integer, ForeignKey('service_categories.id'), nullable=True)

    services = relationship('Services', back_populates='service_categories', uselist=True)
    estate_complexes = relationship('EstateComplexes', secondary='estates_services', back_populates="service_categories")

    def __repr__(self):
        return self.name


class Services(BaseModel):

    """ Услуги """

    __tablename__ = 'services'
    __table_args__ = {"extend_existing": True}

    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    need_validation = Column(Boolean, default=True)
    service_data_schema = Column(String)
    payment_required = Column(Boolean, default=False)

    service_categories_id = Column(Integer, ForeignKey('service_categories.id'), nullable=False)

    service_categories = relationship('ServiceCategories', back_populates='services', uselist=False)
    service_item = relationship('ServiceItems')
    service_requests = relationship('ServiceRequests', uselist=True)

    def __repr__(self):
        return self.name


class ServiceItems(BaseModel):

    """ Доп атрибуты заявок (оплата) """

    __tablename__ = 'service_items'
    __table_args__ = {"extend_existing": True}

    name = Column(String, nullable=False)
    services_id = Column(Integer, ForeignKey('services.id'), nullable=False)
