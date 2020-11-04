import os
import pickle
import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Sets up the bot with a private token that I can't publish
bot = commands.Bot(command_prefix='!')

@bot.command(name='rank')
async def rank(ctx, title, number):
    #####################################################################
    # Copied these lines from Google
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #######################################################################
    sheetName = title + " (event)"
    result = sheet.values().get(spreadsheetId = '1xOMJcEq_fVPQ4VXHfuStVNWAC4tw6d5w6i7VDEcPgn4', range=sheetName).execute()
    values = result.get('values', [])
    firstSpace = True
    secondSpace = True
    for i in range(len(values[0])):
        if values[0][i] == '1':
            rankColumn = i
        if values[0][i] == '':
            if not firstSpace:
                if secondSpace:
                    blankColumn = i
                    secondSpace = False
            else:
                firstSpace = False
    
bot.run(TOKEN)
