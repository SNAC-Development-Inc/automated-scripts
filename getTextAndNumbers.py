import os
import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.errors import HttpError
from datetime import datetime
from functools import reduce


SCOPES = ['https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DISCOVERY_SHEET = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
DOCUMENT_ID = '13vSFaJECdBDmHjRsYjTZgXxR0R_F4m-CnBgnJjt9tFM'
SAMPLE_SPREADSHEET_ID = "1tgB6W50nA90WUGSAhHOhOhk_G0iV6JLSv6MhUo4SNdw"
mikaCredentialsPath = '/Users/nmestrad/Documents/GoogleCredentials/credentials.json'
CREDENTIALS_PATH="/Users/nmestrad/Documents/Keys/client_secret_975762424647-65soulb2m5h4b85o4gke286rjf8jtvfe.apps.googleusercontent.com.json"
SERVICE_ACCOUNT_CREDENTIALS_PATH ="/Users/nmestrad/Documents/Keys/crafty-clover-254716-8282657ec03e.json"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('/Users/nmestrad/Projects/automated-scripts/token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CREDENTIALS_PATH, SCOPES)
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

def is_date(string):
    try:
        datetime.strptime(string, '%m/%d/%Y')
        return True
    except:
        return False

def gatherMessages(parsedText):
    captured_messages = []
    date_indices = [idx for idx, line in enumerate(parsedText) if is_date(line)]
    for idx, dateIdx in enumerate(date_indices):
        if len(date_indices) -1 == idx:
            if len(parsedText) -1  <= dateIdx:
                pass
            else:
                captured_messages.append(parsedText[dateIdx+1:])
        else: 
            startIdx=dateIdx+1
            endIdx=date_indices[idx+1]
            captured_messages.append(parsedText[startIdx:endIdx])

    def combine(message, line):
        if(line): 
            message+=line
        else:
            message+= '\n'
        return message

    # takes the array items from the split messages and uses the combine function to turn them into strings with the new line added
    parsed_messages = [reduce(combine, message).strip() for message in captured_messages]

    return parsed_messages
    
def main():
    """Uses the Docs API to print out the text of a document."""
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build(
        'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    text = read_structural_elements(doc_content)
    print(f"{text}")
    parsedText = text.split('\n')

    messages = gatherMessages(parsedText)
    
    try:
        # Below is the google API docs method of retrieving data from sheets
        sheet_service = discovery.build("sheets", "v4", http=http, discoveryServiceUrl = DISCOVERY_SHEET)

        # Call the Sheets API
        sheet = sheet_service.spreadsheets()
        result = (
            sheet.values().batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=['Sheet1!A2:A','Sheet2!A2:A']).execute()
        )
        # if sheet name not included it always gets the first sheet
        #content = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="A:ZZZ").execute()
        range_values = [range['values'] for range in result.get('valueRanges', [])]
        def parse(x,y):
            x.append(y[0])
            return x
        
        parsed_numbers =[reduce(parse,set) for set in range_values]
        
        phone_numbers = parsed_numbers[0] + parsed_numbers[1]

        if not phone_numbers:
            print("No data found.")
            return
           

    except HttpError as err:
        print(err)

    if not doc_content:
        print('no text')
    # else:
        # Construct the message from the retrieved values
        # message = "\n".join([f"{row[0]}: {row[1]}" for row in values])

        # Recipient's phone number or email associated with iMessage
        #recipient = '2242044024'  # Replace with recipient's phone number

        # Send the message via iMessage
        # was getting a permissions issue with sending the imessage 
        # ran `crsutil disable` in terminal

        # not using py_imessage because of configuration setup for allowing permissions to imessge 
        # imessage.send(recipient, read_structural_elements(doc_content))
        # return list of phone numbers and text message to send

    ## convert phone numbers to applescript list
    ##applescript_list_nums = "{" + ", ".join(map(repr, phone_numbers)) + "}"

    ## applescript reads print values as the return value for a script :-|
    print('|**|'.join(phone_numbers + [messages[0]]))

if __name__ == '__main__':
    main()
