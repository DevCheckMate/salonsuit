from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from salonsuite.database.orm_registry import table_mapper


@table_mapper.mapped_as_dataclass
class ServiceCategory:
    __tablename__ = 'service_category'

    service_category_id: Mapped[int] = mapped_column(
        init=False, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey('status.status_id'), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
