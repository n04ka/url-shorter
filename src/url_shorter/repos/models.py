from datetime import UTC, datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import DateTime, Field, SQLModel, Column
from pydantic import computed_field
from ..generator import to_code_obf
class Link(SQLModel, table=True):
    __tablename__ = "links"  # опционально, можно задать имя таблицы

    id: int | None = Field(default=None, primary_key=True, index=True)
    # short: str = Field(
    #     max_length=5, unique=True, index=True, description="Короткая ссылка"
    # )
    url: str = Field(
        max_length=2000,
        unique=True,
        index=True,
        description="Оригинальный URL",
        
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), 
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
        )

    clicks: int = Field(default=0, description="Количество переходов")
    expires_at: datetime | None = Field(
        default=None, description="Дата истечения ссылки",
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
    )

    @computed_field
    @property
    def code(self) -> str:
        return to_code_obf(self.id)
