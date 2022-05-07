import uuid

from sqlalchemy.orm import declarative_base, registry
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean,  Column, String, event

from authentication.domain import model

Base = declarative_base()

mapper_registry = registry()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    is_banned = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


def start_mappers():
    mapper_registry.map_imperatively(model.User, User)
