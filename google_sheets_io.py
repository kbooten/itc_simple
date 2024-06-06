import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Get the JSON string from the environment variable
from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from a .env file if present
creds_json_string = os.getenv('GOOGLE_CREDS')

# Convert string back to JSON
creds_json = json.loads(creds_json_string)

# Use credentials to create a service account object
creds = service_account.Credentials.from_service_account_info(creds_json)

service = build('sheets', 'v4', credentials=creds)

spreadsheetId="1_vH-JFTVr7VN6kKd0U_eJ7XEsRXvqOQ1vr9Eu-ciGSY"

# import time

# def append_data_to_google_sheet(values, service=service, range_name='interactions_simple_rooms!A1'):
#     try:
#         body = {'values': values}
#         result = service.spreadsheets().values().append(
#             spreadsheetId=spreadsheetId, range=range_name,
#             valueInputOption='RAW', body=body).execute()
#         print(f"{result.get('updates').get('updatedCells')} cells appended.")
#     except Exception as e:
#         print(f"Error appending data to Google Sheet: {e}")


def read_rooms_from_google_sheet(service=service, range_name="rooms_with_instructions!A1:Z100"):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=range_name
    ).execute()
    values = result.get('values', [])
    return values


def main():
    write_field_to_google_sheets()

if __name__ == '__main__':
    main()