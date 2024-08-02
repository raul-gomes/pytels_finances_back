from http import HTTPStatus
from fastapi import Depends, FastAPI
import datetime
from sqlalchemy import select, extract
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


from pytels_finances.database import get_session
from pytels_finances.models.models import IncomeModel
from pytels_finances.schemas.income_schema import IncomeList, IncomeSchema


app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/month/', status_code=HTTPStatus.OK)
def get_month(
    current_month: str = datetime.datetime.now().month,
    session: Session = Depends(get_session)
    ):

    incomes = session.query(IncomeModel).filter(
        extract('month', IncomeModel.date) == current_month
    ).all()

    #{ data: '', descricao: '', icon: '', valor: '' }
    incomes = [{'data': income.date.strftime('%d/%m/%Y'), 'descricao': income.describe, 'icon': '', 'valor': str(income.amount)} for income in incomes ]

    return {'incomes': incomes}

@app.post('/newIncome/', status_code=HTTPStatus.CREATED)
def new_incomes(income: IncomeSchema, session: Session = Depends(get_session)):
    print(income)
    db_user = IncomeModel(
        date=income.date,
        amount=income.amount,
        describe=income.describe
    )
    print(db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
    

@app.post('/newDescrive/', status_code=HTTPStatus.CREATED)
def new_describe():
    ...