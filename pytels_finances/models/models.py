from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry
table_registry = registry()

@table_registry.mapped_as_dataclass
class IncomeModel:
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date: Mapped[datetime]
    amount: Mapped[float]
    describe: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
