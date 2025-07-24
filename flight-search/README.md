# FlightSearch - Modern Flight Price Comparison

A modern, minimalistic flight ticket price search system built with React and Vite, featuring a sleek black and white design.

## Features

- 🎨 Modern, minimalistic black and white design
- ✈️ Real-time flight price comparison
- 📱 Responsive design for all devices
- 🔍 Advanced search filters (passengers, cabin class)
- ⚡ Fast and lightweight with Vite
- 🎯 Clean and intuitive user interface

## Tech Stack

- **Frontend**: React 18
- **Build Tool**: Vite
- **Styling**: CSS3 with modern design patterns
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **API**: RapidAPI Flight Price Comparison

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn
- RapidAPI account and API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flight-search
```

2. Install dependencies:
```bash
npm install
```

3. Configure your RapidAPI key:
   - Sign up at [RapidAPI](https://rapidapi.com)
   - Subscribe to the [Compare Flight Prices API](https://rapidapi.com/obryan-software-obryan-software-default/api/compare-flight-prices)
   - Get your API key from the RapidAPI dashboard

4. Update the API key in the code:
   Open `src/components/FlightSearch.jsx` and replace `'YOUR_RAPIDAPI_KEY'` with your actual RapidAPI key:

```javascript
headers: {
  'X-RapidAPI-Key': 'YOUR_ACTUAL_API_KEY_HERE',
  'X-RapidAPI-Host': 'compare-flight-prices.p.rapidapi.com'
}
```

5. Start the development server:
```bash
npm run dev
```

6. Open your browser and navigate to `http://localhost:5173`

## Usage

1. **Enter Flight Details**:
   - From: Enter departure airport code or city (e.g., JFK, New York)
   - To: Enter destination airport code or city (e.g., LAX, Los Angeles)
   - Date: Select your travel date
   - Passengers: Choose number of passengers (1-8)
   - Cabin Class: Select from Economy, Premium Economy, Business, or First Class

2. **Search Flights**:
   - Click the "Search Flights" button
   - Wait for the API to return flight results
   - View the results displayed in JSON format

## API Configuration

The application uses the Compare Flight Prices API from RapidAPI. The API endpoint accepts the following parameters:

- `from`: Departure location (airport code or city)
- `to`: Destination location (airport code or city)
- `date`: Travel date (YYYY-MM-DD format)
- `passengers`: Number of passengers (1-8)
- `cabinClass`: Cabin class (economy, premium_economy, business, first)

## Project Structure

```
flight-search/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Application header
│   │   └── FlightSearch.jsx    # Main search component
│   ├── App.jsx                 # Main app component
│   ├── App.css                 # Global styles
│   ├── main.jsx                # App entry point
│   └── index.css               # Base styles
├── public/                     # Static assets
├── package.json                # Dependencies and scripts
└── README.md                   # This file
```

## Customization

### Styling
The application uses a custom CSS design system with:
- Black and white color scheme
- Modern card-based layout
- Responsive grid system
- Smooth animations and transitions

### Adding Features
You can easily extend the application by:
- Adding more search filters
- Implementing flight result visualization
- Adding user authentication
- Integrating with booking systems

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure you've replaced `'YOUR_RAPIDAPI_KEY'` with your actual API key
2. **CORS Issues**: The API should handle CORS, but if you encounter issues, check your RapidAPI subscription
3. **No Results**: Verify that the airport codes or city names are correct and supported by the API

### Development

- **Build for production**: `npm run build`
- **Preview production build**: `npm run preview`
- **Lint code**: `npm run lint`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support or questions:
- Check the [RapidAPI documentation](https://rapidapi.com/obryan-software-obryan-software-default/api/compare-flight-prices)
- Review the API response format and error codes
- Ensure your RapidAPI subscription is active
