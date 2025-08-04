def format_date(date_string):
    from datetime import datetime
    
    # Convert date string to a standardized format (YYYY-MM-DD)
    try:
        date_obj = datetime.strptime(date_string, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

def calculate_price_difference(price1, price2):
    # Calculate the difference between two flight prices
    return abs(price1 - price2)