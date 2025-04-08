from sqlalchemy.orm import Session
from datetime import datetime
from . import models

def get_monthly_summary(db: Session, monthly_budget: float):
    today = datetime.today()
    month_start = datetime(today.year, today.month, 1).date()
    
    # Get all transactions for the current month
    transactions = db.query(models.Transaction).filter(models.Transaction.date >= month_start).all()
    
    total_spent = sum(t.amount for t in transactions)
    remaining = monthly_budget - total_spent

    # Daily limit calc
    total_days = 30  # or use calendar module for actual days
    days_left = total_days - today.day + 1
    daily_limit = round(remaining / days_left, 2) if days_left > 0 else 0

    return {
        "monthly_budget": monthly_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining,
        "daily_limit": daily_limit,
        "days_left": days_left
    }
