def rule_based_category(merchant: str):
    merchant = merchant.lower()

    if any(x in merchant for x in ['swiggy', 'zomato', 'domino']):
        return 'Food'
    elif any(x in merchant for x in ['petrol', 'hp', 'indianoil', 'bpcl']):
        return 'Transport'
    elif any(x in merchant for x in ['amazon', 'flipkart']):
        return 'Shopping'
    else:
        return 'Other'
