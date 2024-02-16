import os
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def read_phone_numbers_and_messages_from_google_sheets(sheet_id, sheet_name, column_phone, column_message):
    #1 REPLACE THE X's WITH THE PATH TO YOUR CREDENTIAL FILE DOWNLOADED IN STEP 3 OF THE GUIDE
    credentials_path = "/Users/mtosca/The Solarpunk Project/The Weather Text/Send Bulk SMS/the-weather-text-a9221899f621.json"

    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=credentials)

    range_phone = '{}!{}{}'.format(sheet_name, column_phone, '2')
    range_message = '{}!{}{}'.format(sheet_name, column_message, '2')
    
    result_phone = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_phone).execute()
    result_message = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_message).execute()
    
    phone_numbers = [row[0] for row in result_phone.get('values', [])]
    text_messages = [row[0] for row in result_message.get('values', [])]
    
    return phone_numbers, text_messages

#2 REPLACE THE X's WITH THE GOOGLE SHEET ID
sheet_id = '1gBBgYVX65Kje3UdWA0Do0CCvnRoGpZgk_0zE-rIsi2A'

#3 REPLACE THE X's WITH THE GOOGLE SHEET SHEET NAME
sheet_name = 'Sheet1'

#4 REPLACE THE X's WITH THE LETTER OF THE COLUMN LETTER FOR PHONE NUMBERS  
column_phone = 'A:A'

#5 REPLACE THE X's WITH THE LETTER OF THE COLUMN LETTER FOR THE SMS MESSAGE 
column_message = 'B:B'

phone_numbers, text_messages = read_phone_numbers_and_messages_from_google_sheets(sheet_id, sheet_name, column_phone, column_message)

output = []
for number, message in zip(phone_numbers, text_messages):
    output.append('{} {}|**|'.format(number.strip(), message.strip()))

print(''.join(output))

