import os
#import csv
# To run this on Mika's PC do we need to install these packages?? how would we do this?
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from py_imessage import imessage

credentialsPath = '/Users/nmestrad/Documents/Keys/client_secret_975762424647-65soulb2m5h4b85o4gke286rjf8jtvfe.apps.googleusercontent.com.json'

# credentials = service_account.Credentials.from_service_account_file(
#     credentialsPath)
# # Authenticate using your credentials.json file for Google Docs API
# credentials = credentials.from_authorized_user_file(credentialsPath, scopes=['https://www.googleapis.com/auth/documents.readonly'])

# # Create the Docs API service
# service = build('docs', 'v1', credentials=credentials)

# # Authenticate using your credentials.json file for Google Sheets API
# #credentials = Credentials.from_authorized_user_file(credentialsPath, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

# # Create the Sheets API service
# #service = build('sheets', 'v4', credentials=credentials) 

# # The ID of the spreadsheet you want to access
# document_id = '13vSFaJECdBDmHjRsYjTZgXxR0R_F4m-CnBgnJjt9tFM'

# # Call the Docs API to get the document content
# document = service.documents().get(documentId=document_id).execute()

# # Extract the text content from the document
# text_content = ''
# for content in document.get('body').get('content'):
#     if 'paragraph' in content:
#         for element in content['paragraph']['elements']:
#             text_content += element['textRun']['content']

# # Print or process the text content as needed
# print('data recieved')

# The range of cells you want to retrieve data from
#range_name = 'Sheet1!A1:B10'  # Example: Sheet1 is the name of the sheet, A1:B10 is the range

# Call the Sheets API to get the values
# result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
# values = result.get('values', [])

# if not values:
#     print('No data found in the spreadsheet.')
# else:
#     # Construct the message from the retrieved values
#     message = "\n".join([f"{row[0]}: {row[1]}" for row in values])

#     # Recipient's phone number or email associated with iMessage
#     recipient = '1234567890'  # Replace with recipient's phone number

#     # Send the message via iMessage
#     imessage.send(recipient, message)
#     print("Message sent successfully!")

import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from py_imessage import imessage

SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = '13vSFaJECdBDmHjRsYjTZgXxR0R_F4m-CnBgnJjt9tFM'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(credentialsPath, SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def main():
    """Uses the Docs API to print out the text of a document."""
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build(
        'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    print(read_structural_elements(doc_content))
    if not doc_content:
        print('no text')
    else:
        # Construct the message from the retrieved values
        # message = "\n".join([f"{row[0]}: {row[1]}" for row in values])

        # Recipient's phone number or email associated with iMessage
        recipient = '2242044024'  # Replace with recipient's phone number

        # Send the message via iMessage
        # was getting a permissions issue with sending the imessage 
        # ran `crsutil disable` in terminal

        imessage.send(recipient, read_structural_elements(doc_content))
        print("Message sent successfully!")

if __name__ == '__main__':
    main()
