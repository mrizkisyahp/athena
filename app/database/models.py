from datetime import datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.responsibilities.models import (
    ResponsibilityPriority,
    ResponsibilityStatus,
)


class Base(DeclarativeBase):
    pass


class ResponsibilityORM(Base):
    __tablename__ = "responsibilities"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    status: Mapped[ResponsibilityStatus] = mapped_column(
        Enum(ResponsibilityStatus)
    )

    priority: Mapped[ResponsibilityPriority] = mapped_column(
        Enum(ResponsibilityPriority)
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
