from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from salonsuite.database.orm_registry import table_mapper


@table_mapper.mapped_as_dataclass
class UserGroup:
    __tablename__ = 'user_group'

    user_group_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_group_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_group_created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    user_group_updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    user_group_deleted_at: Mapped[datetime] = mapped_column(nullable=False)
