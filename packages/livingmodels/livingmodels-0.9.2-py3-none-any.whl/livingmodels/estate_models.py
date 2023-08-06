from sqlalchemy import (Column, Integer, String, ForeignKey, Float, Enum)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class EstatesServices(BaseModel):

    """  Таблица связи сервисов и недвижимости """

    __tablename__ = 'estates_services'

    estate_complex_id = Column(Integer, ForeignKey('estate_complexes.id'))
    service_categories_id = Column(Integer, ForeignKey('service_categories.id'))

    __table_args__ = (
        {"extend_existing": True},
    )

    def __str__(self):
        return f'{self.permission} for {self.role}'


class EstateComplexes(BaseModel):

    """  Справочник объектов недвижимости """

    __tablename__ = 'estate_complexes'
    __table_args__ = {"extend_existing": True}

    estate_complex_name = Column(String, nullable=False)
    house_management_company_id = Column(Integer, ForeignKey('house_management_company.id'), nullable=False)

    house_management_company = relationship('HouseManagementCompany', back_populates='estate_complexes', uselist=False)
    service_categories = relationship('ServiceCategories', secondary='estates_services',
                                      back_populates="estate_complexes")
    buildings = relationship('Buildings', back_populates='estate_complex', uselist=True)
    # apartments = relationship('Apartments', back_populates='apartment_complex', order_by='Apartments.apartment_number',
    #                           uselist=True)


class Buildings(BaseModel):

    """  Справочник сооружений комплекса """

    __tablename__ = 'buildings'
    __table_args__ = {"extend_existing": True}

    building_name = Column(String, nullable=False)
    estate_complexes_id = Column(Integer, ForeignKey('estate_complexes.id'), nullable=False)

    estate_complex = relationship('EstateComplexes', back_populates='buildings', uselist=False)
    apartments = relationship('Apartments', back_populates='building', uselist=True, lazy='joined')


class Apartments(BaseModel):

    """  Справочник помещений """

    __tablename__ = 'apartments'
    __table_args__ = {"extend_existing": True}

    apartment_number = Column(Integer, nullable=False)
    apartment_type = Column(String, nullable=False)
    apartment_area = Column(Float, nullable=False)
    hallway_area = Column(Float, nullable=False)
    tenants_number = Column(Integer)
    estate_complexes_id = Column(Integer, ForeignKey('estate_complexes.id'), nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)

    # apartment_complex = relationship('EstateComplexes', back_populates='apartments', uselist=False)
    building = relationship('Buildings', back_populates='apartments', uselist=False)
