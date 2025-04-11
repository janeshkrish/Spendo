from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from app.summary import get_spending_summary

router = APIRouter()

@router.delete("/reset")
def reset_transactions(db: Session = Depends(get_db)):
    db.query(models.Transaction).delete()
    db.commit()
    return {"message": "All transactions have been reset."}

@router.get("/summary")
def summary():
    return get_spending_summary()