import os
import re
import boto3
import pandas as pd
from pathlib import Path

# Determine the absolute paths for input and output files
base_dir = Path(__file__).resolve().parent
csv_output_path = base_dir / "../data/processed/survivor_vote_off_quotes.csv"
json_output_path = base_dir / "../data/processed/survivor_vote_off_quotes.json"

# Load the data
voteoff_df = pd.read_json("https://stilesdata.com/survivor/survivor_vote_off_reactions.json")

def clean_quote(quote):
    # Check if the quote is a string and not null
    if not isinstance(quote, str) or quote == '':
        return ''
    
    # Remove leading/trailing whitespace and quotes
    quote = quote.strip().strip('"').strip()
    
    # Ensure there is proper punctuation at the end of the sentence
    if not re.search(r'[.!?]$', quote):
        quote += '.'
    
    # Capitalize the first letter of each sentence
    quote = '. '.join(sentence.capitalize() for sentence in quote.split('. '))
    
    return quote

# Apply the cleaning function to the ack_quote column
voteoff_df['ack_quote_clean'] = voteoff_df['ack_quote'].apply(lambda x: clean_quote(x))

quotes_df = voteoff_df[voteoff_df['ack_quote'] != ""].copy()

PROCESSED_COLS = ['season', 'season_name', 'episode', 'gender', 'castaway_id', 'castaway', 'full_name', 'acknowledge', 'ack_score', 'ack_quote_clean']

df_processed = quotes_df[PROCESSED_COLS].copy()

"""
Export to local storage and upload to S3
"""

# Save to CSV & JSON
df_processed.to_csv(csv_output_path, index=False)
df_processed.to_json(json_output_path, orient='records', lines=False, indent=4)
print(f"Data saved to {csv_output_path} and {json_output_path}")

# Upload CSV and JSON to S3
s3_bucket = 'stilesdata.com'
s3_csv_key = 'survivor/survivor_vote_off_quotes.csv'
s3_json_key = 'survivor/survivor_vote_off_quotes.json'

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