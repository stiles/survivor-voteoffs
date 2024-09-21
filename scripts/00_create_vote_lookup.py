import os
import pandas as pd
from pathlib import Path
import boto3

# Determine the absolute paths for input and output files
base_dir = Path(__file__).resolve().parent
csv_output_path = base_dir / "../data/processed/survivor_vote_off_order.csv"
json_output_path = base_dir / "../data/processed/survivor_vote_off_order.json"

# Read vote history table from the [survivoR2py repo](https://github.com/stiles/survivoR2py)
vote_history_df = pd.read_csv(
    "https://raw.githubusercontent.com/stiles/survivoR2py/main/data/processed/csv/vote_history.csv",
    dtype={"season": str, "vote": str, "episode": str},
)

# Filter for distinct values to create a vote off lookup
vote_offs = (
    vote_history_df.query(f'version == "US"')[
        ["season", "season_name", "episode", "voted_out", "voted_out_id", "version"]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Running vote count by season
vote_offs["vote"] = vote_offs.groupby("season")["voted_out"].cumcount() + 1

# Clean up data types
# vote_offs["episode"] = vote_offs["episode"].astype(str)
# vote_offs["season"] = vote_offs["season"].astype(str)
# vote_offs["vote"] = vote_offs["vote"].astype(str)

# Add a bit more information about castaway to the dataframe
castaway_details_df = pd.read_csv(
    "https://raw.githubusercontent.com/stiles/survivoR2py/main/data/processed/csv/castaway_details.csv"
)

# Merge the vote off order and castaway bio details
vote_offs_merged = pd.merge(
    vote_offs,
    castaway_details_df[
        [
            "castaway_id",
            "full_name",
            "date_of_birth",
            "gender",
            "personality_type",
            "occupation",
        ]
    ],
    left_on="voted_out_id",
    right_on="castaway_id",
)

"""
Export to local storage and upload to S3
"""

# Store locally as CSV & JSON
vote_offs_merged.to_csv(csv_output_path, index=False)
vote_offs_merged.to_json(json_output_path, orient='records', lines=False, indent=4)

# Paths for S3 storage
s3_bucket = 'stilesdata.com'
s3_csv_key = 'survivor/survivor_vote_off_order.csv'
s3_json_key = 'survivor/survivor_vote_off_order.json'

# Initialize boto3 client with environment variables
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('MY_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('MY_AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('MY_AWS_SESSION_TOKEN')
)

# Upload the CSV file to S3
s3_client.upload_file(str(csv_output_path), s3_bucket, s3_csv_key)
print(f"CSV file uploaded to s3://{s3_bucket}/{s3_csv_key}")

# Upload the JSON file
s3_client.upload_file(str(json_output_path), s3_bucket, s3_json_key)
print(f"JSON file uploaded to s3://{s3_bucket}/{s3_json_key}")