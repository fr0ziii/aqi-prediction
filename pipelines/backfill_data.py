from fetch_data import fetch_raw_data
from compute_features import process_raw_data
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("AQICN_API_TOKEN")
CITY = "barcelona"

# Backfill function
def backfill_data(start_date, end_date):
    """
    Fetch and process data for a range of dates to backfill historical data.
    
    Parameters:
        start_date (str): The start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
    """
    all_data = []

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        try:
            # Fetch raw data (API might not support date-specific queries)
            raw_data = fetch_raw_data(CITY, API_TOKEN)

            # Process raw data into features
            processed_data = process_raw_data(raw_data)
            
            # Add the current date as a column
            processed_data["historical_date"] = current_date.strftime("%Y-%m-%d")
            all_data.append(processed_data)

            print(f"Fetched and processed data for {current_date.strftime('%Y-%m-%d')}")

        except Exception as e:
            print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')}: {e}")

        # Increment the date
        current_date += timedelta(days=1)

    # Combine all data into a single DataFrame
    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)

        # Ensure the end_date is formatted to 'YYYY-MM-DD' (without time)
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Save to a CSV file without the time component in the file name
        output_path = f"data/backfilled_data_{start_date}_to_{end_date_str}.csv"
        os.makedirs("data", exist_ok=True)
        final_data.to_csv(output_path, index=False)
        print(f"Backfilled data saved to {output_path}")
    else:
        print("No data fetched during the backfill process.")

# Run the backfill process
if __name__ == "__main__":
    START_DATE = "2025-01-20"  # Adjust as needed
    END_DATE = "2025-01-27"    # Adjust as needed
    backfill_data(START_DATE, END_DATE)
