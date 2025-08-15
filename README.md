# ✈️ Award Travel Value Calculator

A Python web tool that suggests optimal travel redemptions using synthetic routing and comprehensive analysis.

## 🎯 Features

- **Value Calculator**: Compare flights vs. hotels vs. gift cards
- **Synthetic Routing**: Find cost-effective routes through major hubs
- **Comprehensive Analysis**: Rank all redemption options by value
- **Web Interface**: Interactive search with real-time data

## 🚀 Quick Start

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python app.py`
3. **Access**: `http://localhost:5001`

## 🔧 How It Works

1. **Input**: Origin, destination, dates, loyalty program, points
2. **Analysis**: Generates flight, hotel, gift card, and synthetic routing options
3. **Calculation**: Computes value-per-point for each option
4. **Output**: Ranked recommendations by highest value

## 📊 Example Results

- ✈️ 8 direct flight options
- 🏨 4 hotel redemption options  
- 🎁 4 gift card options
- 🔄 4 synthetic routing options
- **Total**: 20 redemption options analyzed

## 🏗️ Architecture

- **Flask** web framework
- **Real-time TPG scraping**
- **Multi-API integration** with fallbacks
- **Mock data generators** for testing
- **Responsive Bootstrap UI**

## 📁 Files

- `app.py` - Main Flask application
- `real_data_integration.py` - Core analysis engine
- `templates/` - HTML templates
- `config.py` - Configuration & API keys

## 🧪 Testing

```bash
# Test import
python -c "from real_data_integration import RealDataIntegration; print('Success!')"

# Test analysis
python -c "from real_data_integration import RealDataIntegration; real_data = RealDataIntegration(); analysis = real_data.get_comprehensive_redemption_analysis('JFK', 'LAX', '2024-12-20'); print(f'{len(analysis)} options found')"
```

## 📖 Documentation

See [COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md) for detailed technical documentation.

---

**Built for travel enthusiasts and points hackers** 🎉
