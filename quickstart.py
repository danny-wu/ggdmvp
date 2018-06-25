"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime

import collect_worldbank

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1WtrQyyBruznqkpZz0SIztisMyIvYXK-T6JrpcqZKKEU'

def update_sheet(sheet_name, api_url, add_last=False):
    data = collect_worldbank.collect(api_url, add_last)
    body = {'values': data}

    result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=sheet_name + '!A5',
    valueInputOption='USER_ENTERED',
    body=body).execute()

    print('Updated data for {}'.format(sheet_name))
    update_last_updated(sheet_name)


def update_last_updated(sheet):
    last_updated_body = {'values': [[str(datetime.now())]]}

    # Update last updated
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='{}!D1'.format(sheet),
        valueInputOption='USER_ENTERED',
        body=last_updated_body).execute()

# update_sheet('Population', 'http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv')
# update_sheet('Unemployment', 'http://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv')
# update_sheet('Poverty', 'http://api.worldbank.org/v2/en/indicator/SI.POV.DDAY?downloadformat=csv', True)
# update_sheet('Renewable Consumption', 'http://api.worldbank.org/v2/en/indicator/EG.FEC.RNEW.ZS?downloadformat=csv')
update_sheet('Renewable Output', 'http://api.worldbank.org/v2/en/indicator/EG.ELC.RNEW.ZS?downloadformat=csv')