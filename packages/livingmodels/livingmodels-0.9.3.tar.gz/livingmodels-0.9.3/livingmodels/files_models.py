from sqlalchemy import (Column, Integer, String, ForeignKey, Enum)
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .schemas.files_schema import AccessFilesRules


class NextcloudFiles(BaseModel):

    """  Хранение файлов в сервисе Nextcloud """

    __tablename__ = 'nextcloud_files'
    __table_args__ = {"extend_existing": True}

    file_name = Column(String, nullable=False)
    file_type = Column(String, default='New', nullable=False)
    file_path = Column(String, nullable=False)
    size = Column(Integer, nullable=True)
    access = Column(Enum(AccessFilesRules), default='internal')
    expire = Column(Integer, default=24)

    service_requests_id = Column(Integer, ForeignKey('service_requests.id'))
    service_requests = relationship('ServiceRequests', back_populates='files', uselist=False)
