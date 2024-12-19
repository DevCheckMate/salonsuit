from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from salonsuite.database.orm_registry import table_mapper
from salonsuite.utils.enum import UserStatus


@table_mapper.mapped_as_dataclass
class Users:
    __tablename__ = 'users'

    users_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey('user_group.user_group_id'), nullable=True
    )
    cellphone: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    pin: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    birthdate: Mapped[date] = mapped_column(nullable=True)
    instagram: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(String(6), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status_id: Mapped[int] = mapped_column(
        ForeignKey('user_status.user_status_id'),
        nullable=False,
        default=UserStatus.ATIVO.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True, default=None
    )
