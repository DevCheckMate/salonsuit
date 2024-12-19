from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from salonsuite.database.orm_registry import table_mapper


@table_mapper.mapped_as_dataclass
class Status:
    __tablename__ = 'status'

    status_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
