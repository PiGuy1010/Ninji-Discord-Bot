import os
import pickle
import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from discord.ext import commands

with open("token.txt") as fin:
    TOKEN = fin.read()
bot = commands.Bot(command_prefix='!')

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

@bot.command(name='eventrank')
async def time(ctx, title, position):
    rank = int(position)
    print(rank)
    if rank < 1 or rank > 100:
        await ctx.send("You entered either a non-positive rank or a rank above 100, which are not allowed.")
        raise Exception("You entered either a non-positive rank or a rank above 100, which are not allowed.")
    try:
        # Call the Sheets API
        sheet = service.spreadsheets()

        sheetName = title + " (event)"
        result = sheet.values().get(spreadsheetId = '1xOMJcEq_fVPQ4VXHfuStVNWAC4tw6d5w6i7VDEcPgn4', range=sheetName).execute()
        values = result.get('values', [])
        for i in range(3, len(values[0])):
            if values[0][i] == '':
                blankColumn = i
                break
        timeColumn = blankColumn-1
        firstRow = 0
        while (values[firstRow] == [] or values[firstRow][1] == ''):
            firstRow += 1
            if firstRow >= 100:
                raise Exception("Empty")
                break
        if rank < firstRow+1:
            await ctx.send(f"Rank {rank} in {sheetName} is not exactly known, but we do know that Rank {firstRow+1} is {values[firstRow][timeColumn]} seconds.")
        else:
            prev = values[firstRow][1]
            prevRow = firstRow
            didSomething = False
            for i in range(firstRow, 100):
                if values[i] != [] and values[i][1] != '' and not "?" in values[i][1]:
                    if int(values[i][1]) == rank:
                        print("Found exact rank")
                        didSomething = True
                        await ctx.send(f"Rank {rank} in {sheetName} is {values[i][timeColumn]} seconds.")
                        break
                    elif int(values[i][1]) > rank:
                        print("Found greater rank")
                        didSomething = True
                        await ctx.send(f"Rank {rank} in {sheetName} is not exactly known, but we do know that Rank {prev} is {values[prevRow][timeColumn]} seconds and Rank {i+1} is {values[i][timeColumn]} seconds.")
                        break
                    else:
                        prev = values[i][1]
                        prevRow = i
            print("Got to line 73")
            if not didSomething:
                await ctx.send(f"Rank {rank} in {sheetName} is not exactly known, but we do know that Rank {prev} is {values[prevRow][timeColumn]} seconds.")
    except:
        await ctx.send("Some error occurred (most likely typoed or autocorrected title). Please use this command in the form !rank (title) (position).")
@bot.command(name='rank')
async def knowntime(ctx,title,position):
    rank = int(position)-1
    print(rank)
    if rank < 0:
        await ctx.send("You entered a non-positive rank, which is not allowed")
        raise Exception("You entered a non-positive rank, which is not allowed")
    try:

        #Call the Sheets API
        sheet = service.spreadsheets()
        #######################################################################
        sheetName = title
        result = sheet.values().get(spreadsheetId = '1xOMJcEq_fVPQ4VXHfuStVNWAC4tw6d5w6i7VDEcPgn4', range=sheetName).execute()
        values = result.get('values', [])
        timeColumn = 5
        playerColumn = 3
        if rank < len(values):
            await ctx.send(f"Rank {rank+1} in {sheetName} is {values[rank][timeColumn]} by {values[rank-1
            ][playerColumn]}")
        else:
            await ctx.send("There aren't that many known times")
    except:
        await ctx.send("some error occured (most likely typoed or autocorrected title). Please use this command in the form !rank (title) (position)")
bot.run(TOKEN)
