from datetime import date, datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from salonsuite.database.orm_registry import table_mapper


@table_mapper.mapped_as_dataclass
class Users:
    __tablename__ = 'users'

    users_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    users_email: Mapped[str] = mapped_column(String(255), nullable=True)
    users_name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int] = mapped_column(nullable=True)
    users_cellphone: Mapped[str] = mapped_column(String(11), nullable=False)
    users_pin: Mapped[str] = mapped_column(String(11), nullable=False)
    users_password: Mapped[str] = mapped_column(String(255), nullable=False)
    users_birthdate: Mapped[date] = mapped_column(nullable=True)
    users_instagram: Mapped[str] = mapped_column(String(100), nullable=True)
    users_gender: Mapped[str] = mapped_column(String(6), nullable=True)
    users_description: Mapped[str] = mapped_column(String(255), nullable=True)
    status_id: Mapped[int] = mapped_column(
        ForeignKey('status.status_id'), nullable=False
    )
    users_image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    users_created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    users_update_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    users_deleted_at: Mapped[datetime] = mapped_column(nullable=True)
