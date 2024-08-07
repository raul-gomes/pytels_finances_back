from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class DescribeSchema(BaseModel):
    describe: str

class IncomeInputSchema(BaseModel):
    date: datetime
    amount: float
    describe: str
    isNewDescribe: bool
    newDescribe: str

class IncomeOutputSchema(BaseModel):
    date: str
    amount: float
    describe: str
    model_config = ConfigDict(from_attributes=True)

class IncomeResponseSchema(BaseModel):
    incomes: list[IncomeOutputSchema]

class NewIncomeResponseSchema(BaseModel):
    incomes: IncomeOutputSchema

class DescribesResponseSchema(BaseModel):
    describes: list[str]
    