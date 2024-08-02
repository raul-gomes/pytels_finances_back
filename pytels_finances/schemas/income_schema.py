from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IncomeSchema(BaseModel):
    date: datetime
    amount: float
    describe: str


class IncomePublic(BaseModel):
    date: datetime
    amount: float
    describe: str
    model_config = ConfigDict(from_attributes=True)

class IncomeList(BaseModel):
    incomes: list[IncomePublic]