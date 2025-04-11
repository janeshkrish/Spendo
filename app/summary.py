from sqlalchemy.orm import Session
from datetime import datetime
from . import models
from app.database import SessionLocal
from app.models import Transaction
from sqlalchemy import func


def get_monthly_summary(db: Session, monthly_budget: float):
    today = datetime.today()
    month_start = datetime(today.year, today.month, 1).date()
    
    # Get all transactions for the current month
    transactions = db.query(models.Transaction).filter(models.Transaction.date >= month_start).all()
    
    total_spent = sum(t.amount for t in transactions)
    remaining = monthly_budget - total_spent

    # Daily limit calc
    total_days = 30  # You can use calendar.monthrange() for actual days if needed
    days_left = total_days - today.day + 1
    daily_limit = round(remaining / days_left, 2) if days_left > 0 else 0

    # Alerts
    alerts = []
    if remaining < 0:
        alerts.append("⚠️ You’ve exceeded your monthly budget!")
    if daily_limit < 0:
        alerts.append("⚠️ You are overspending! Adjust your expenses.")

    return {
        "monthly_budget": monthly_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining,
        "daily_limit": daily_limit,
        "days_left": days_left,
        "alerts": alerts
    }
def get_spending_summary():
    db = SessionLocal()
    summary = db.query(Transaction.category, func.sum(Transaction.amount))\
                .group_by(Transaction.category).all()
    db.close()

    return {
        "summary": [
            {"category": category, "total": total}
            for category, total in summary
        ]
    }
