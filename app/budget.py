from datetime import datetime
import calendar

def get_daily_limit(monthly_budget, total_spent):
    today = datetime.today().day
    total_days = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
    days_left = total_days - today + 1
    remaining = monthly_budget - total_spent
    per_day = max(0, round(remaining / days_left, 2))
    return per_day, days_left, remaining
