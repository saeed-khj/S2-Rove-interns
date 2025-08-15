#!/usr/bin/env python3
"""
Test script for Award Travel Value Calculator
"""

import requests
import time
import json

def test_web_app():
    """Test the web application"""
    print("Testing Award Travel Value Calculator...")
    
    # Wait a moment for the app to start
    time.sleep(3)
    
    try:
        # Test the main page
        response = requests.get('http://localhost:5001/', timeout=10)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
            
        # Test the search functionality with sample data
        search_data = {
            'origin': 'JFK',
            'destination': 'LAX',
            'date': '2024-02-15',
            'cabin': 'economy',
            'trip_type': 'oneway'
        }
        
        response = requests.post('http://localhost:5001/search', data=search_data, timeout=15)
        if response.status_code == 200:
            print("✅ Search functionality works")
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
            
        print("🎉 All tests passed! The application is working correctly.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Make sure it's running on http://localhost:5001")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_web_app() 