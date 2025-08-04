# Travel API Tool

## Overview
The Travel API Tool is an integration tool designed to retrieve, process, and store travel data, specifically focusing on flight information. This project connects to the Amadeus API to fetch real-time flight data, processes it for analysis, and stores it in a database for easy retrieval.

## Features
- Connects to the Amadeus API to retrieve flight data.
- Processes and filters flight data based on user-defined criteria.
- Stores processed data in a database for future analysis.
- Utility functions for date formatting and price calculations.

## Project Structure
```
travel-api-tool
├── src
│   ├── main.py            # Entry point of the application
│   ├── api
│   │   └── client.py      # API client for connecting to Amadeus API
│   ├── processing
│   │   └── processor.py    # Data processing logic
│   ├── storage
│   │   └── database.py     # Database connection and data storage
│   └── utils
│       └── helpers.py      # Utility functions
├── datasets
│   └── sample_routes.csv   # Sample datasets for selected routes
├── docs
│   └── synthetic_routing_briefing.md  # Document briefing about synthetic routing
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/travel-api-tool.git
   ```
2. Navigate to the project directory:
   ```
   cd travel-api-tool
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.