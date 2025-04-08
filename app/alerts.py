from sqlalchemy.orm import Session
from datetime import datetime
from . import models

def check_alerts(db: Session, monthly_budget: float):
    today = datetime.today()
    month_start = datetime(today.year, today.month, 1).date()

    # Get all transactions for the current month
    transactions = db.query(models.Transaction).filter(models.Transaction.date >= month_start).all()

    total_spent = sum(t.amount for t in transactions)
    remaining = monthly_budget - total_spent
    total_days = 30
    days_left = total_days - today.day + 1
    daily_limit = remaining / days_left if days_left > 0 else 0

    # Get today's spend
    today_spent = sum(t.amount for t in transactions if t.date.date() == today.date())


    alerts = []

    # Check monthly overspend
    if total_spent > monthly_budget:
        alerts.append("⚠️ You have exceeded your monthly budget!")

    # Check daily overspend
    if today_spent > daily_limit:
        alerts.append("⚠️ Today’s spending exceeds your daily limit!")

    # Check high-value transactions (> ₹1000)
    high_txns = [t for t in transactions if t.amount > 1000]
    if high_txns:
        alerts.append(f"💸 {len(high_txns)} high-value transaction(s) detected this month.")

    return {
        "today_spent": today_spent,
        "daily_limit": round(daily_limit, 2),
        "alerts": alerts
    }
