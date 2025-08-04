# Travel API Tool

## Overview
Travel API Tool is a Python application for collecting, processing, and storing flight data from the Amadeus API. It allows users to gather flight information for selected routes over a specified month, extract key details, and save them in a local SQLite database for analysis or reporting.

## Features
- Connects to the Amadeus API using secure authentication.
- Retrieves flight offers for multiple user-defined routes and dates.
- Processes flight data to extract price, airline, departure time, and date.
- Saves all processed flight details in a local SQLite database (`travel_data.db`).
- Modular code structure for easy maintenance and extension.

## Project Structure
```
travel-api-tool
├── src
│   ├── main.py                # Main application script
│   ├── api
│   │   └── client.py          # Amadeus API client
│   ├── processing
│   │   └── processor.py       # Data processing logic
│   ├── storage
│   │   └── database.py        # SQLite database handler
│   └── utils
│       └── helpers.py         # Utility functions
├── datasets
│   └── sample_routes.csv      # Example route data
├── docs
│   └── synthetic_routing_briefing.md # Synthetic routing documentation
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/saeed-khj/travel-api-tool.git
   ```
2. Change to the project directory:
   ```
   cd travel-api-tool
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application and start collecting flight data:
```
python src/main.py
```
- The script will collect flight data for the routes and dates specified in `main.py`.
- All results will be saved in `travel_data.db` in your project folder.

## Database

- The SQLite database (`travel_data.db`) stores all flight details.
- You can view or query the database using Python, DB Browser for SQLite, or any SQLite-compatible tool.

## Contributing

Contributions and suggestions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.