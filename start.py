#!/usr/bin/env python3
"""
Startup script for Award Travel Value Calculator
"""

import os
import sys
import subprocess
import time
import webbrowser

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'flask': 'flask',
        'requests': 'requests', 
        'beautifulsoup4': 'bs4',
        'pandas': 'pandas',
        'lxml': 'lxml'
    }
    
    missing_packages = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def start_application():
    """Start the Flask application"""
    print("🚀 Starting Award Travel Value Calculator...")
    print("📱 The application will be available at: http://localhost:5001")
    print("⏳ Starting server...")
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("✈️  Award Travel Value Calculator")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    print("🎯 Features:")
    print("   • Real-time TPG point valuations")
    print("   • Award flight comparisons")
    print("   • Cash price analysis")
    print("   • Value-per-mile calculations")
    print("   • Smart recommendations")
    print()
    
    # Ask user if they want to open browser automatically
    try:
        response = input("🌐 Open browser automatically when app starts? (y/n): ").lower().strip()
        auto_open = response in ['y', 'yes']
    except KeyboardInterrupt:
        auto_open = False
    
    if auto_open:
        # Wait a moment then open browser
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:5001')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    
    print()
    print("💡 Tips:")
    print("   • Use 3-letter airport codes (e.g., JFK, LAX, LHR)")
    print("   • Try different cabin classes for better comparisons")
    print("   • Check the 'Update TPG Values' button for fresh data")
    print()
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main() 