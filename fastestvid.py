@bot.command(name='fastestvid')
async def findfastvid(ctx,title):
    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        #######################################################################
        sheetName = title
        result = sheet.values().get(spreadsheetId='1xOMJcEq_fVPQ4VXHfuStVNWAC4tw6d5w6i7VDEcPgn4',
                                    range=sheetName).execute()
        values = result.get('values', [])
        resultLink = sheet.values().get(spreadsheetId='1xOMJcEq_fVPQ4VXHfuStVNWAC4tw6d5w6i7VDEcPgn4',
                                    range=sheetName,fields="sheets/data/rowData/values/hyperlink").execute()
        valuesLink = resultLink.get('values', [])

        for i in range(len(values[0])):
            if values[1][i] == "Fastest Time with Video" or values[1][i] == "Fastest Full Run with Video":
                timeColumn = i
        for i in range(timeColumn):
            if valuesLink[2][timeColumn-i] == "":
                timeColumn -= 1
            else:
                break

        await ctx.send(f"fastest video is {values[2][timeColumn]}")
    except:
        await ctx.send("some error occured (most likely typoed or autocorrected title). Please use this command in the form !fastestvid (title)")
