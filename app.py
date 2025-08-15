from flask import Flask, render_template, request, jsonify, flash
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import os
from tpg_scraper import scrape_tpg_point_values, get_tpg_values
from award_hacker import get_award_data
from sky_scrapper import get_cash_price
from value_calculator import calculate_value_comparison
from config import get_airports, get_airports_by_country, get_airport_by_code, CACHE_DURATION, PORT, DEBUG_MODE

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global variables for caching
TPG_VALUES_CACHE = None
TPG_CACHE_TIMESTAMP = None

@app.route('/')
def index():
    """Main page with search form"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests and return results"""
    try:
        # Get form data
        origin = request.form.get('origin', '').strip().upper()
        destination = request.form.get('destination', '').strip().upper()
        date = request.form.get('date')
        cabin = request.form.get('cabin', 'economy')
        trip_type = request.form.get('trip_type', 'oneway')
        return_date = request.form.get('return_date') if trip_type == 'roundtrip' else None
        
        # Validate inputs
        if not all([origin, destination, date]):
            flash('Please fill in all required fields (Origin, Destination, Date)', 'error')
            return render_template('index.html')
        
        # Update TPG values if needed
        update_tpg_values()
        
        # Get award data
        award_results = get_award_data(origin, destination, cabin)
        
        if not award_results:
            flash('No award flights found for this route. Please try different airports or dates.', 'error')
            return render_template('index.html')
        
        # Get cash price
        cash_price_data = get_cash_price(origin, destination, date)
        
        if not cash_price_data:
            flash('Unable to fetch cash prices. Please try again later.', 'error')
            return render_template('index.html')
        
        # Calculate values
        results = calculate_value_comparison(
            award_results, 
            cash_price_data, 
            TPG_VALUES_CACHE,
            trip_type,
            return_date
        )
        
        return render_template('results.html', 
                             results=results, 
                             search_params={
                                 'origin': origin,
                                 'destination': destination,
                                 'date': date,
                                 'cabin': cabin,
                                 'trip_type': trip_type,
                                 'return_date': return_date
                             })
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/comprehensive-analysis', methods=['POST'])
def comprehensive_analysis():
    """Handle comprehensive redemption analysis including flights, hotels, gift cards, and synthetic routing"""
    try:
        # Get form data
        origin = request.form.get('origin', '').strip().upper()
        destination = request.form.get('destination', '').strip().upper()
        date = request.form.get('date')
        return_date = request.form.get('return_date')
        loyalty_program = request.form.get('loyalty_program', 'American Airlines')
        points_available = int(request.form.get('points_available', 100000))
        
        # Validate inputs
        if not all([origin, destination, date]):
            flash('Please fill in all required fields (Origin, Destination, Date)', 'error')
            return render_template('index.html')
        
        # Import the comprehensive analysis function
        from real_data_integration import RealDataIntegration
        real_data = RealDataIntegration()
        
        # Get comprehensive redemption analysis
        all_redemptions = real_data.get_comprehensive_redemption_analysis(
            origin, destination, date, return_date, loyalty_program, points_available
        )
        
        if not all_redemptions:
            flash('No redemption options found for this route. Please try different airports or dates.', 'error')
            return render_template('index.html')
        
        # Group redemptions by type for better organization
        redemption_groups = {
            'direct_flights': [],
            'hotels': [],
            'gift_cards': [],
            'synthetic_routing': []
        }
        
        for redemption in all_redemptions:
            redemption_type = redemption.get('redemption_type', 'unknown')
            if redemption_type in redemption_groups:
                redemption_groups[redemption_type].append(redemption)
        
        return render_template('comprehensive_results.html', 
                             redemptions=all_redemptions,
                             redemption_groups=redemption_groups,
                             search_params={
                                 'origin': origin,
                                 'destination': destination,
                                 'date': date,
                                 'return_date': return_date,
                                 'loyalty_program': loyalty_program,
                                 'points_available': points_available
                             })
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/api/airports')
def get_airports_api():
    """API endpoint to get airport suggestions"""
    # Get query parameters for filtering
    country = request.args.get('country')
    search = request.args.get('search', '').upper()
    
    if country:
        airports = get_airports_by_country(country)
    else:
        airports = get_airports()
    
    # Filter by search term if provided
    if search:
        airports = [
            airport for airport in airports 
            if search in airport['code'] or search in airport['city'].upper() or search in airport['name'].upper()
        ]
    
    return jsonify(airports)

@app.route('/update-tpg')
def update_tpg():
    """Manual endpoint to update TPG values"""
    try:
        update_tpg_values(force_update=True)
        flash('TPG point values updated successfully!', 'success')
    except Exception as e:
        flash(f'Failed to update TPG values: {str(e)}', 'error')
    
    return render_template('index.html')

def update_tpg_values(force_update=False):
    """Update TPG values if cache is expired or forced"""
    global TPG_VALUES_CACHE, TPG_CACHE_TIMESTAMP
    
    current_time = time.time()
    
    if (force_update or 
        TPG_VALUES_CACHE is None or 
        TPG_CACHE_TIMESTAMP is None or 
        current_time - TPG_CACHE_TIMESTAMP > CACHE_DURATION):
        
        try:
            TPG_VALUES_CACHE = scrape_tpg_point_values()
            TPG_CACHE_TIMESTAMP = current_time
            print("TPG values updated successfully")
        except Exception as e:
            print(f"Failed to update TPG values: {e}")
            # Try to load from existing CSV file
            if os.path.exists('tpg_point_values.csv'):
                TPG_VALUES_CACHE = pd.read_csv('tpg_point_values.csv')
                TPG_CACHE_TIMESTAMP = current_time

if __name__ == '__main__':
    # Initialize TPG values on startup
    update_tpg_values()
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=PORT) 