from pydantic import BaseModel
from datetime import datetime


class OutcomeRequestSquema(BaseModel):
    amount: float
    cardType: str
    date: datetime
    describe: str
    installments: int
    outcomeType: str
    recurrency: bool

class OutcomeSquema(BaseModel):
    amount: float
    cardType: str
    date: datetime
    describe: str
    outcomeType: str

class OutcomeResponseSquema(BaseModel):
    outcome: OutcomeSquema

