import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Load the client secrets file
service_account_file = os.path.expanduser("~/.google_service_account.json")

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
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_output_path = os.path.join(base_dir, "../data/processed/survivor_vote_off_reactions.csv")
json_output_path = os.path.join(base_dir, "../data/processed/survivor_vote_off_reactions.json")
vote_offs_lookup_path = os.path.join(base_dir, "../data/processed/survivor_voteoff_order.csv")

# Open the Google Spreadsheet by name
spreadsheet_name = "survivor_vote_offs"
spreadsheet = client.open(spreadsheet_name).get_worksheet(0)

# Fetch data from the worksheet
data = spreadsheet.get_all_records()

data_entry = pd.DataFrame(data)

# Clean castaways table
vote_offs_lookup = pd.read_csv(vote_offs_lookup_path)

# Assertion to ensure the lengths are the same
assert len(data_entry) == len(
    vote_offs_lookup
), f"Assertion failed: Lengths do not match (data_entry: {len(data_entry)}, vote_offs_lookup: {len(vote_offs_lookup)}"

print("Lengths match successfully!")

# Merge them together to add ids to Google Sheet
merged = pd.merge(
    data_entry, vote_offs_lookup, on=["season", "vote"], how="right", indicator=True
)
merged["match"] = merged["castaway"] == merged["voted_out"]

assert merged[
    "match"
].all(), "Assertion failed: There are mismatched rows in the DataFrame."

print("All rows matched successfully!")

# List of columns to convert
bool_columns = ["acknowledge", "ack_gesture", "ack_speak", "ack_look", "ack_smile"]

# Convert the columns from string to boolean
for col in bool_columns:
    merged[col] = merged[col].map({"TRUE": True, "FALSE": False})

# Define acknowledgment columns
ack_columns = ["ack_gesture", "ack_speak", "ack_look", "ack_smile"]

# Calculate acknowledgment score as the count of True values in the acknowledgment columns
merged["ack_score"] = merged[ack_columns].sum(axis=1)

clean_cols = ['season', 'vote', 'episode', 'castaway', 'voted_out_id', 'acknowledge', 'ack_gesture', 'ack_speak',
       'ack_look', 'ack_smile', 'ack_speak_notes', 'ack_score', 'notes']

merged_clean = merged[clean_cols].rename(columns={'voted_out_id': 'castaway_id'}).copy()

# Save to CSV
merged_clean.to_csv(csv_output_path, index=False)

# Save to JSON
merged_clean.to_json(json_output_path, orient='records', lines=False, indent=4)

print(f"Data saved to {csv_output_path} and {json_output_path}")