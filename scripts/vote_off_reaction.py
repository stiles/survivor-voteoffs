import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import boto3

# Load the client secrets file
service_account_file = Path.home() / ".google_service_account.json"

# Define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Authenticate using the service account file
credentials = Credentials.from_service_account_file(service_account_file, scopes=scope)

# Authorize the gspread client
client = gspread.authorize(credentials)

"""
FETCH & SCORE
How did contestants respond after their torch was snuffed? 
This script fetches the growing log and scores the acknowledgement of his/her tribe.
"""

# Determine the absolute paths for input and output files
base_dir = Path(__file__).resolve().parent
csv_output_path = base_dir / "../data/processed/survivor_vote_off_reactions.csv"
json_output_path = base_dir / "../data/processed/survivor_vote_off_reactions.json"
vote_offs_lookup_path = base_dir / "../data/processed/survivor_vote_off_order.csv"

try:
    # Open the Google Spreadsheet by name
    spreadsheet_name = "survivor_vote_offs"
    spreadsheet = client.open(spreadsheet_name).get_worksheet(0)

    # Fetch data from the worksheet
    data = spreadsheet.get_all_records()

    # Convert data to DataFrame
    data_entry = pd.DataFrame(data)

    # Clean castaways table
    vote_offs_lookup = pd.read_csv(vote_offs_lookup_path)

    # Assertion to ensure the lengths are the same
    assert len(data_entry) == len(vote_offs_lookup), (
        f"Assertion failed: Lengths do not match (data_entry: {len(data_entry)}, "
        f"vote_offs_lookup: {len(vote_offs_lookup)})"
    )

    print("Lengths match successfully!")

    # Merge them together to add ids to Google Sheet
    merged = pd.merge(
        data_entry, vote_offs_lookup, on=["season", "vote"], how="right", indicator=True
    )
    merged["match"] = merged["castaway"] == merged["voted_out"]

    assert merged["match"].all(), "Assertion failed: There are mismatched rows in the DataFrame."

    print("All rows matched successfully!")

    # List of columns to convert
    bool_columns = ["acknowledge", "ack_gesture", "ack_speak", "ack_look", "ack_smile"]

    # Convert the columns from string to boolean
    merged[bool_columns] = merged[bool_columns] == "TRUE"

    # Define acknowledgment columns
    ack_columns = ["ack_gesture", "ack_speak", "ack_look", "ack_smile"]

    # Calculate acknowledgment score as the count of True values in the acknowledgment columns
    merged["ack_score"] = merged[ack_columns].sum(axis=1)

    clean_cols = [
        'season', 'vote', 'episode', 'castaway', 'voted_out_id', 'acknowledge', 'ack_gesture', 
        'ack_speak', 'ack_look', 'ack_smile', 'ack_speak_notes', 'ack_score', 'notes'
    ]

    merged_clean = merged[clean_cols].rename(columns={'voted_out_id': 'castaway_id'}).copy()

    # Save to CSV
    merged_clean.to_csv(csv_output_path, index=False)

    # Save to JSON
    merged_clean.to_json(json_output_path, orient='records', lines=False, indent=4)

    print(f"Data saved to {csv_output_path} and {json_output_path}")

    # Upload CSV and JSON to S3
    s3_bucket = 'stilesdata.com'
    s3_csv_key = 'survivor/survivor_vote_off_reactions.csv'
    s3_json_key = 'survivor/survivor_vote_off_reactions.json'

    # Initialize boto3 client with environment variables
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('MY_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('MY_AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('MY_AWS_SESSION_TOKEN')
    )

    # Upload the CSV file
    s3_client.upload_file(str(csv_output_path), s3_bucket, s3_csv_key)
    print(f"CSV file uploaded to s3://{s3_bucket}/{s3_csv_key}")

    # Upload the JSON file
    s3_client.upload_file(str(json_output_path), s3_bucket, s3_json_key)
    print(f"JSON file uploaded to s3://{s3_bucket}/{s3_json_key}")

except Exception as e:
    print(f"An error occurred: {e}")
