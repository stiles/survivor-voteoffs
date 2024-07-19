import os
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
How did contestants respond after they were voted off?  
This script fetches a Google sheet with hand-curated data
for each vote, adds some basic details about the season
and castaway and then scores how each one acknowledged their tribe
after Jeff snuffed their torches.
"""

# Determine the absolute paths for input and output files
base_dir = Path(__file__).resolve().parent
csv_output_path = base_dir / "../data/processed/survivor_vote_off_reactions.csv"
json_output_path = base_dir / "../data/processed/survivor_vote_off_reactions.json"
vote_offs_lookup_url = "https://stilesdata.com/survivor/survivor_vote_off_order.json"

# Open the Google sheet with vote-off details by the file name
spreadsheet_name = "survivor_vote_offs"
spreadsheet = client.open(spreadsheet_name).get_worksheet(0)

# Fetch data from the worksheet and convert data to DataFrame
data = spreadsheet.get_all_records()
data_entry_df = pd.DataFrame(data)

# Separately, read a castaway details table
vote_offs_lookup = pd.read_json(vote_offs_lookup_url)

# Merge them together to add castaway ids and season names to the Google sheet
merged = pd.merge(data_entry_df, vote_offs_lookup, on=["season", "vote"])

# Convert season and episode to integers, then back to strings to remove the .0 suffix
merged["season"] = merged["season"].astype(int).astype(str)
merged["episode"] = merged["episode"].astype(int).astype(str)

# List of columns to convert
bool_columns = ["acknowledge", "ack_gesture", "ack_speak", "ack_look", "ack_smile"]

# Convert the columns from string to boolean
merged[bool_columns] = merged[bool_columns] == "TRUE"

# Define acknowledgment columns
ack_columns = ["ack_gesture", "ack_speak", "ack_look", "ack_smile"]

# Calculate acknowledgment score as the count of True values in the acknowledgment columns
merged["ack_score"] = merged[ack_columns].sum(axis=1)

merged_slim = merged[['season', 'season_name', 'vote', 'episode', 'castaway', 'full_name', 'castaway_id', 'gender', 'date_of_birth',
                      'personality_type', 'occupation', 'acknowledge', 'ack_look', 'ack_speak',
                      'ack_gesture', 'ack_smile', 'ack_speak_notes', 'ack_score']].copy()

"""
Export to local storage and upload to S3
"""

# Save to CSV & JSON
merged_slim.to_csv(csv_output_path, index=False)
merged_slim.to_json(json_output_path, orient='records', lines=False, indent=4)
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