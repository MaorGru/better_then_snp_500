# Better Than S&P 500

## Overview

Better Than S&P 500 is a Python-based project designed to provide predictions and insights into financial markets. The project aims to outperform the S&P 500 index by leveraging advanced data analysis and prediction models.

## Features

- **API Endpoints**: Expose prediction capabilities via RESTful APIs.
- **Prediction Models**: Utilize advanced machine learning models for market predictions.
- **Market Data Integration**: Fetch and process data from various market sources.
- **Logging and Error Handling**: Robust logging and error management for better debugging and monitoring.

## Project Structure

```
app/
    main.py          # Entry point of the application
    api/             # API-related modules
    clients/         # External data clients
    core/            # Core utilities and configurations
    schemas/         # Data models and schemas
    services/        # Business logic and services
    tests/           # Unit and integration tests
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MaorGru/better_then_snp_500.git
   ```
2. Navigate to the project directory:
   ```bash
   cd better_then_snp_500
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python app/main.py
```

## Testing

Run the test suite:

```bash
pytest
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## API Endpoints

### Predict Endpoint

The predict endpoint allows users to compare a stock's performance against the S&P 500 index.

- **URL**: `/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "symbol": "AAPL",
    "date": "2025-08-23"
  }
  ```
- **Response**:

  ```json
  {
    "symbol": "AAPL",
    "date": "2025-08-23",
    "prediction": true,
    "confidence": 1
  }
  ```

- **Description**: This endpoint takes a stock symbol and a reference date as input and returns whether the stock is predicted to outperform the S&P 500 index on the given date, along with a confidence score.
