from mock_utl import *

import discord
from discord_utl import *
from discord_imp import *

#########################################################################################################
# Global definitions

MOCK_TRIGGER = '!mock'

try:
    tokenFile = open('environment/.env', 'r')
    helpMenuFile = open('environment/help_menu.txt', 'r')
except Exception as ex:
    print('Exception caught attempting to open environment files')
    print('Please verify .env and help_menu.txt files exist and are in the correct location')
    print('Exiting..')
    print(str(ex))
    exit(1)

try:
    BOT_TOKEN = tokenFile.read()
    HELP_MENU = helpMenuFile.read()
except Exception as ex:
    print('Exception caught attempting to read environment files')
    print('Exiting..')
    print(str(ex))
    exit(1)

client = discord.Client()
    
#########################################################################################################
# On_message handler - Executes after message is detected
#
# Parameters
# message: Message (Discord API)

@client.event
async def on_message(message):
    spaceDelimMessage = message.content.split(' ')

    # Message isn't from mock bot and message includes !mock
    if (client.user != message.author) and (spaceDelimMessage[0] == MOCK_TRIGGER):
        await deleteMessage(message)
        msgWithoutTrg = message.content.replace('!mock ', '')

        # Prompts user to provide command if not provided
        if len(spaceDelimMessage) <= 1:
            await sendMessage(client.user, message.channel, 'Please provide a command\nUse ***!mock help*** for a help menu')

        # Help menu
        elif spaceDelimMessage[1] == 'help':
            await sendMessage(client.user, message.channel, HELP_MENU)

        # Mock a specific message
        elif ('https://discordapp.com/channels' in spaceDelimMessage[1]):
            fetchedMessage = await fetchMessage(client.user, message.channel, spaceDelimMessage[1])
            
            if fetchedMessage is not None:
                mockedMessage = MoCk(fetchedMessage.content)
                await sendMessage(client.user, message.channel, mockedMessage)
            else:
                await sendMessage(client.user, message.channel, 'Failed to mock targeted message')
        
        # Mock x number of messages of target user
        elif len(message.mentions) > 0:
            targetUser = message.mentions[0]
            numOfMessages = await getNumOfMsgs(msgWithoutTrg)
            
            if numOfMessages > 10:
                await sendMessage(client.user, message.channel, 'MoCk BoT can only mock 10 messages or less at a time')
            else:
                messageHistory = await getMessageHistory(client.user, message.channel, 1000)

                if messageHistory is not None:
                    if numOfMessages == -1:
                        filterMessages = filterMessageHistory(messageHistory, targetUser, 1)
                    else:
                        filterMessages = filterMessageHistory(messageHistory, targetUser, numOfMessages)
                    
                    for msg in filterMessages:
                        mockedMessage = MoCk(msg.content)
                        await sendMessage(client.user, message.channel, targetUser.mention + ' ' + mockedMessage)
                else:
                    await sendMessage(client.user, message.channel, 'Failed to mock historical message(s)')
        
        # Mock provided message
        else:
            mockedMessage = MoCk(msgWithoutTrg)
            await sendMessage(client.user, message.channel, mockedMessage)

#########################################################################################################
# On_ready handler - Executes after bot starts up

@client.event
async def on_ready():
    print(f'{client.user} has connected')

#########################################################################################################
# Startup command to start the bot

client.run(BOT_TOKEN)