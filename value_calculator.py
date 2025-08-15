import pandas as pd
import math

def calculate_value_comparison(award_data, cash_data, tpg_values, trip_type='oneway', return_date=None):
    """
    Calculate value comparison between award flights and cash prices
    
    Args:
        award_data: List of award flight options
        cash_data: List of cash flight options
        tpg_values: DataFrame with TPG point valuations
        trip_type: 'oneway' or 'roundtrip'
        return_date: Return date for round trips
    
    Returns:
        List of comparison results
    """
    results = []
    
    # Get the lowest cash price for comparison
    if cash_data:
        lowest_cash_price = min([flight['price'] for flight in cash_data])
    else:
        lowest_cash_price = 0
    
    # Calculate round trip multiplier
    trip_multiplier = 2 if trip_type == 'roundtrip' else 1
    
    for award in award_data:
        try:
            # Get TPG baseline value for this program
            tpg_baseline = get_tpg_baseline_value(award['program'], tpg_values)
            
            # Calculate total cost for award flight
            total_award_cost = (award['miles'] * trip_multiplier, award['taxes'] * trip_multiplier)
            
            # Calculate value per mile
            value_per_mile = calculate_value_per_mile(
                lowest_cash_price * trip_multiplier, 
                total_award_cost[1], 
                total_award_cost[0]
            )
            
            # Determine verdict
            verdict = determine_verdict(value_per_mile, tpg_baseline)
            
            # Calculate savings
            savings = calculate_savings(
                lowest_cash_price * trip_multiplier,
                total_award_cost[0],
                total_award_cost[1],
                tpg_baseline
            )
            
            result = {
                'airline': award['airline'],
                'program': award['program'],
                'miles_required': total_award_cost[0],
                'taxes': total_award_cost[1],
                'cash_price': lowest_cash_price * trip_multiplier,
                'value_per_mile': value_per_mile,
                'tpg_baseline': tpg_baseline,
                'verdict': verdict,
                'savings': savings,
                'availability': award.get('availability', 'Unknown'),
                'transfer_partners': award.get('transfer_partners', []),
                'trip_type': trip_type,
                'return_date': return_date
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"Error calculating value for {award['program']}: {e}")
            continue
    
    # Sort results by value per mile (best first)
    results.sort(key=lambda x: x['value_per_mile'], reverse=True)
    
    return results

def get_tpg_baseline_value(program_name, tpg_values):
    """
    Get TPG baseline value for a specific program
    """
    if tpg_values is None or tpg_values.empty:
        return get_default_tpg_value(program_name)
    
    # Create a mapping of program names to handle variations
    program_mapping = {
        # Airline programs
        'American AAdvantage': 'American Airlines AAdvantage',
        'United MileagePlus': 'United MileagePlus',
        'Delta SkyMiles': 'Delta SkyMiles',
        'British Airways Avios': 'Avios',
        'Air Canada Aeroplan': 'Air Canada Aeroplan',
        'Alaska Airlines Mileage Plan': 'Alaska Airlines Mileage Plan',
        'Southwest Rapid Rewards': 'Southwest Rapid Rewards',
        'JetBlue TrueBlue': 'JetBlue TrueBlue',
        'Spirit Airlines Free Spirit': 'Spirit Airlines Free Spirit',
        'Frontier Miles': 'Frontier Miles',
        'Hawaiian Airlines HawaiianMiles': 'HawaiianMiles',
        'Korean Air SkyPass': 'Korean Air SkyPass',
        'Qantas Frequent Flyer': 'Qantas Frequent Flyer',
        'Singapore Airlines KrisFlyer': 'Singapore Airlines KrisFlyer',
        'Turkish Airlines Miles&Smiles': 'Turkish Airlines Miles&Smiles',
        'Virgin Atlantic Flying Club': 'Virgin Atlantic Flying Club',
        'Emirates Skywards': 'Emirates Skywards',
        'Etihad Guest': 'Etihad Guest',
        'Flying Blue': 'Flying Blue',
        'Cathay Asia Miles': 'Cathay Asia Miles',
        'ANA Mileage Club': 'ANA Mileage Club',
        'Avianca LifeMiles': 'Avianca LifeMiles',
        'Aeromexico Rewards': 'Aeromexico Rewards',
        
        # Credit card programs
        'Chase Ultimate Rewards': 'Chase Ultimate Rewards',
        'American Express Membership Rewards': 'American Express Membership Rewards',
        'Citi ThankYou Rewards': 'Citi ThankYou Rewards',
        'Capital One': 'Capital One',
        'Wells Fargo Rewards': 'Wells Fargo Rewards',
        'Bilt Rewards': 'Bilt Rewards',
        
        # Hotel programs
        'Hilton Honors': 'Hilton Honors',
        'Marriott Bonvoy': 'Marriott Bonvoy',
        'World of Hyatt': 'World of Hyatt',
        'IHG One Rewards': 'IHG One Rewards',
        'Wyndham Rewards': 'Wyndham Rewards',
        'Best Western Rewards': 'Best Western Rewards',
        'Choice Privileges': 'Choice Privileges',
        'Accor Live Limitless': 'Accor Live Limitless'
    }
    
    # Try exact match first
    match = tpg_values[tpg_values['program_name'] == program_name]
    if not match.empty:
        return match.iloc[0]['value_per_point']
    
    # Try mapped name
    mapped_name = program_mapping.get(program_name)
    if mapped_name:
        match = tpg_values[tpg_values['program_name'] == mapped_name]
        if not match.empty:
            return match.iloc[0]['value_per_point']
    
    # Try partial matches (case insensitive)
    program_name_lower = program_name.lower()
    for _, row in tpg_values.iterrows():
        csv_name_lower = row['program_name'].lower()
        
        # Check if program name contains key words from CSV
        if (program_name_lower in csv_name_lower or 
            csv_name_lower in program_name_lower or
            any(word in csv_name_lower for word in program_name_lower.split() if len(word) > 3)):
            return row['value_per_point']
    
    # Try reverse mapping (check if CSV name maps to our program)
    for csv_name, mapped_program in program_mapping.items():
        if mapped_program == program_name:
            match = tpg_values[tpg_values['program_name'] == csv_name]
            if not match.empty:
                return match.iloc[0]['value_per_point']
    
    # Return default value if no match found
    print(f"⚠️  No TPG value found for '{program_name}', using default")
    return get_default_tpg_value(program_name)

def get_default_tpg_value(program_name):
    """
    Get default TPG value for a program if not found in scraped data
    """
    default_values = {
        'American AAdvantage': 0.014,
        'United MileagePlus': 0.012,
        'Delta SkyMiles': 0.011,
        'British Airways Avios': 0.012,
        'Air Canada Aeroplan': 0.013,
        'Alaska Airlines Mileage Plan': 0.014,
        'Southwest Rapid Rewards': 0.013,
        'JetBlue TrueBlue': 0.012,
        'Hilton Honors': 0.005,
        'Marriott Bonvoy': 0.008,
        'Hyatt World of Hyatt': 0.017,
        'Chase Ultimate Rewards': 0.015,
        'American Express Membership Rewards': 0.015,
        'Citi ThankYou Points': 0.014,
        'Capital One Miles': 0.014
    }
    
    # Try exact match
    if program_name in default_values:
        return default_values[program_name]
    
    # Try partial matches
    for key, value in default_values.items():
        if key.lower() in program_name.lower() or program_name.lower() in key.lower():
            return value
    
    # Default fallback
    return 0.012

def calculate_value_per_mile(cash_price, taxes, miles_required):
    """
    Calculate value per mile using the formula: (cash_price - taxes) / miles_required
    """
    if miles_required <= 0:
        return 0
    
    value = (cash_price - taxes) / miles_required
    return round(value, 4)

def determine_verdict(value_per_mile, tpg_baseline):
    """
    Determine whether to use points or cash based on value per mile vs TPG baseline
    """
    if value_per_mile >= tpg_baseline * 1.1:  # 10% buffer above baseline
        return "Use Points"
    elif value_per_mile >= tpg_baseline * 0.9:  # Within 10% of baseline
        return "Good Value"
    else:
        return "Use Cash"

def calculate_savings(cash_price, miles_required, taxes, tpg_baseline):
    """
    Calculate potential savings when using points vs cash
    """
    # Value of miles at TPG baseline
    miles_value = miles_required * tpg_baseline
    
    # Total cost with points
    total_points_cost = miles_value + taxes
    
    # Savings
    savings = cash_price - total_points_cost
    
    return round(savings, 2)

def calculate_redemption_value(award_data, cash_data, tpg_values):
    """
    Calculate redemption value for different scenarios
    """
    scenarios = []
    
    for award in award_data:
        # Find matching cash flight
        matching_cash = find_matching_cash_flight(award, cash_data)
        
        if matching_cash:
            value_per_mile = calculate_value_per_mile(
                matching_cash['price'],
                award['taxes'],
                award['miles']
            )
            
            tpg_baseline = get_tpg_baseline_value(award['program'], tpg_values)
            
            scenario = {
                'program': award['program'],
                'airline': award['airline'],
                'cash_price': matching_cash['price'],
                'award_cost': award['taxes'],
                'miles_used': award['miles'],
                'value_per_mile': value_per_mile,
                'tpg_baseline': tpg_baseline,
                'redemption_rate': (value_per_mile / tpg_baseline) * 100 if tpg_baseline > 0 else 0
            }
            
            scenarios.append(scenario)
    
    return scenarios

def find_matching_cash_flight(award, cash_data):
    """
    Find the best matching cash flight for comparison
    """
    if not cash_data:
        return None
    
    # Try to find exact airline match first
    for flight in cash_data:
        if award['airline'].lower() in flight['airline'].lower():
            return flight
    
    # Return cheapest flight if no airline match
    return min(cash_data, key=lambda x: x['price'])

def calculate_optimal_strategy(award_data, cash_data, tpg_values, budget=None):
    """
    Calculate optimal strategy based on available options and budget
    """
    comparisons = calculate_value_comparison(award_data, cash_data, tpg_values)
    
    # Filter by budget if specified
    if budget:
        comparisons = [c for c in comparisons if c['taxes'] <= budget]
    
    if not comparisons:
        return None
    
    # Find best value option
    best_option = max(comparisons, key=lambda x: x['value_per_mile'])
    
    # Calculate alternative scenarios
    scenarios = {
        'best_value': best_option,
        'lowest_cost': min(comparisons, key=lambda x: x['taxes']),
        'highest_savings': max(comparisons, key=lambda x: x['savings']),
        'all_options': comparisons
    }
    
    return scenarios

def format_currency(amount):
    """
    Format amount as currency
    """
    return f"${amount:,.2f}"

def format_percentage(value, baseline):
    """
    Format value as percentage of baseline
    """
    if baseline == 0:
        return "N/A"
    percentage = (value / baseline) * 100
    return f"{percentage:.1f}%"

if __name__ == "__main__":
    # Test the value calculator
    test_award_data = [
        {
            'airline': 'American Airlines',
            'program': 'American AAdvantage',
            'miles': 25000,
            'taxes': 50,
            'availability': 'Good'
        }
    ]
    
    test_cash_data = [
        {
            'airline': 'American Airlines',
            'price': 350,
            'cabin_class': 'Economy'
        }
    ]
    
    test_tpg_values = pd.DataFrame([
        {'program_name': 'American AAdvantage', 'value_per_point': 0.014}
    ])
    
    results = calculate_value_comparison(test_award_data, test_cash_data, test_tpg_values)
    print("Test Results:")
    for result in results:
        print(f"{result['program']}: {result['value_per_mile']:.4f} per mile, Verdict: {result['verdict']}") 