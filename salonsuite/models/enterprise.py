from datetime import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from salonsuite.database.orm_registry import table_mapper
from typing import Optional

from salonsuite.utils.enum import Status

@table_mapper.mapped_as_dataclass
class EnterPrise:
    __tablename__ = "enterprise"

    enterprise_id : Mapped[int] = mapped_column(init=False, primary_key=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    cnpj : Mapped[str] = mapped_column(String(14), nullable=False)
    cellphone : Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    email : Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    state : Mapped[str] = mapped_column(String(100), nullable=False)
    city : Mapped[str] = mapped_column(String(100), nullable=False)
    cep : Mapped[str] = mapped_column(String(8), nullable=False)
    status_id : Mapped[int] = mapped_column(ForeignKey('status.status_id'), 
                                            nullable=False, 
                                            default=Status.ATIVO.value)
    deleted_at : Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    created_at : Mapped[datetime] = mapped_column(init= False, server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(init=False, server_default=func.now(), 
                                                  onupdate=func.now())