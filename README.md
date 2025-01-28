# AQI Prediction Project
This project predicts the Air Quality Index (AQI) for the next 3 days using a serverless stack.

## Project Structure
- **feature_pipeline**: Scripts to fetch data, compute features, and store them.
- **tests**: Unit tests for the scripts.
- **data**: Local storage for raw and processed data (temporary).

## Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:
   ```pip install -r requirements.txt