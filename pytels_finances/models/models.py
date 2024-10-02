from datetime import datetime
from typing import List
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
table_registry = registry()

@table_registry.mapped_as_dataclass
class IncomeModel:
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date: Mapped[datetime]
    amount: Mapped[float]
    describe = relationship('DescribeModel', back_populates='income')
    describe_id: Mapped[int] = mapped_column(ForeignKey('describes.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

@table_registry.mapped_as_dataclass
class DescribeModel:
    __tablename__ = 'describes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    describe: Mapped[str]
    income = relationship('IncomeModel', back_populates='describe')


@table_registry.mapped_as_dataclass
class OutcomeModel:
    __tablename__: 'outcomes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date: Mapped[datetime]
    amount: Mapped[float]
    cardtype: Mapped[str]
    installments: Mapped[int]
    recurrency: Mapped[bool]
    create_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

@table_registry.mapped_as_dataclass
class DescribeOutcome:
    ...

@table_registry.mapped_as_dataclass
class OutcomeType:
    ...
