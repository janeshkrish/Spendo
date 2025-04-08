from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    sms_text: str

class TransactionOut(BaseModel):
    amount: float
    date: date
    category: str
    merchant: str
