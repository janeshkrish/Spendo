from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schema, parser, categorize
from fastapi import Query
from .summary import get_monthly_summary
from .alerts import check_alerts
from fastapi import Body
from .parser import parse_sms, categorize_receiver
from .models import Transaction
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Transaction
import re


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class SMSRequest(BaseModel):
    sms_text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transaction")
def parse_sms(request: SMSRequest, db=Depends(get_db)):
    text = request.sms_text

    # Basic pattern matching
    amount_match = re.search(r"debited by (\d+\.?\d*)", text)
    date_match = re.search(r"on date (\d{1,2}[A-Za-z]{3}\d{2})", text)
    merchant_match = re.search(r"trf to (.+?) Refno", text)

    if not amount_match or not date_match or not merchant_match:
        return {"error": "Could not parse SMS"}

    amount = float(amount_match.group(1))
    date_str = date_match.group(1)
    date = datetime.strptime(date_str, "%d%b%y").date()
    merchant = merchant_match.group(1)

    # Optional: category from keyword
    category = "Food" if "swiggy" in merchant.lower() else "Others"

    txn = Transaction(
        amount=amount,
        date=date,
        category=category,
        merchant=merchant
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    return {
        "amount": txn.amount,
        "date": txn.date,
        "category": txn.category,
        "merchant": txn.merchant
    }

@app.get("/summary")
def summary(budget: float = Query(...), db: Session = Depends(get_db)):
    return get_monthly_summary(db, monthly_budget=budget)

@app.get("/alerts")
def alerts(budget: float = Query(...), db: Session = Depends(get_db)):
    return check_alerts(db, monthly_budget=budget)

@app.post("/parse_and_save")
def parse_and_save_sms(msg: str = Body(...), db: Session = Depends(get_db)):
    parsed = parse_sms(msg)
    category = categorize_receiver(parsed['receiver'])

    txn = Transaction(
        amount=parsed['amount'],
        category=category,
        date=parsed['date']
    )
    db.add(txn)
    db.commit()

    return {"status": "success", "parsed": parsed, "category": category}

from app.database import Base, engine
Base.metadata.create_all(bind=engine)