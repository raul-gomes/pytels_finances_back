from http import HTTPStatus
from fastapi import Depends, FastAPI
import datetime
from sqlalchemy import asc, select, extract
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware


from pytels_finances.database import get_session
from pytels_finances.models.models import DescribeModel, IncomeModel
from pytels_finances.schemas.income_schema import DescribesResponseSchema, IncomeResponseSchema, IncomeOutputSchema, IncomeInputSchema, NewIncomeResponseSchema
from pytels_finances.schemas.outcome_schema import OutcomeRequestSquema, OutcomeResponseSquema, OutcomeSquema


app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/month/', status_code=HTTPStatus.OK, response_model=IncomeResponseSchema)
def get_month(
    current_month: str = datetime.datetime.now().month,
    session: Session = Depends(get_session)
    ):

    incomes = session.query(IncomeModel).options(
        joinedload(IncomeModel.describe)
    ).filter(
        extract('month', IncomeModel.date) == current_month
    ).order_by(asc(IncomeModel.date)).all()

    incomes = [
         IncomeOutputSchema(
             date=income.date.strftime("%d-%m-%Y"),
             amount=income.amount,
             describe=income.describe.describe
         )
         for income in incomes
    ]

    return {'incomes': incomes}

@app.post('/newIncome/', status_code=HTTPStatus.CREATED, response_model=NewIncomeResponseSchema)
def new_incomes(income: IncomeInputSchema, session: Session = Depends(get_session)):

    if income.isNewDescribe:
        db_describe = DescribeModel(describe=income.newDescribe)
        session.add(db_describe)
        session.commit()
        session.refresh(db_describe)
    else: 
        stmt = select(DescribeModel).where(DescribeModel.describe == income.describe)
        db_describe = session.execute(stmt).scalar()

    db_income = IncomeModel(
        date=income.date,
        amount=income.amount,
        describe_id=db_describe.id
    )

    session.add(db_income)
    session.commit()
    session.refresh(db_income)


    return {'incomes': IncomeOutputSchema(
                        date = db_income.date.strftime("%d-%m-%Y"),
                        amount = db_income.amount,
                        describe = db_describe.describe
                    )}

@app.get('/getDescribes/', status_code=HTTPStatus.OK, response_model=DescribesResponseSchema)
def get_describe(session: Session = Depends(get_session)):
    smtm = select(DescribeModel)
    describes = [describe.describe for describe in session.execute(smtm).scalars().all()]
    return {'describes': describes}

@app.post('/newOutcome', status_code=HTTPStatus.CREATED, response_model=OutcomeResponseSquema)
def new_outcome(outcome: OutcomeRequestSquema, session: Session = Depends(get_session)):
    print(outcome)
    
    db_outcome = OutcomeSquema(
        amount = 12345,
        cardType = 'debito',
        date = '2024-08-01',
        describe = 'testando 1',
        outcomeType = 'testando 2',
    )
    return {'outcome': outcome}