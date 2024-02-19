import os
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

doc_id = "1eKyiPNUf9yIz3kyU3vHgHTpOpM92DfQi0vEaxFoRjms"

def read_phone_numbers_and_messages_from_google_sheets(sheet_id, sheet_name, column_phone, column_message):
    #1 REPLACE THE X's WITH THE PATH TO YOUR CREDENTIAL FILE DOWNLOADED IN STEP 3 OF THE GUIDE
    credentials_path = '/Users/nmestrad/Documents/GoogleCredentials/mika-google-credentials.json'

    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/documents.readonly'])
    sheet_service = build('sheets', 'v4', credentials=credentials)
    doc_service = build('docs', 'v1', credentials=credentials)
    doc = doc_service.documents().get(documentId=doc_id).execute()

    range_phone = '{}!{}{}'.format(sheet_name, column_phone, '2')
    range_message = '{}!{}{}'.format(sheet_name, column_message, '2')
    
    result_phone = sheet_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_phone).execute()
    result_message = sheet_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_message).execute()
    
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

