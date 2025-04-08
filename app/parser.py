import re
from datetime import datetime

def parse_sms(msg: str):
    # Extract amount
    amount_match = re.search(r"debited by (\d+\.?\d*)", msg)
    amount = float(amount_match.group(1)) if amount_match else 0.0

    # Extract date (e.g., 14Mar25)
    date_match = re.search(r"on date (\d{2}[A-Za-z]{3}\d{2})", msg)
    date_str = date_match.group(1)
    date_obj = datetime.strptime(date_str, "%d%b%y") if date_match else datetime.now()

    # Extract receiver (e.g., Swiggy Limited)
    receiver_match = re.search(r"trf to (.*?) Refno", msg)
    receiver = receiver_match.group(1).strip() if receiver_match else "Unknown"

    return {
        "amount": amount,
        "receiver": receiver,
        "date": date_obj
    }

def categorize_receiver(receiver: str) -> str:
    mapping = {
        "Swiggy": "Food",
        "Zomato": "Food",
        "Bharat Petroleum": "Fuel",
        "Amazon": "Shopping"
    }
    for key in mapping:
        if key.lower() in receiver.lower():
            return mapping[key]
    return "Others"
