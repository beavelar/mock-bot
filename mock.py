import re
import discord

#########################################################################################################
# Global definitions

MOCK_TRIGGER = '!mock'

try:
    tokenFile = open('.env', 'r')
    helpMenuFile = open('help_menu.txt', 'r')
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
# Mock function to mock incoming message

def MoCk(message):
    mock = ""
    cap = True

    for char in message:
        if char == ' ':
            mock += ' '
        else:
            if cap:
                mock += char.upper()
            else:
                mock += char.lower()
            
            cap = not cap
    
    return mock

#########################################################################################################
# Parses and returns the number of messages to mock

async def getNumOfMsgs(channel, message):
    numberOfMessages = -1

    try:
        parsedMessage = message.split('>')
        parsedMessage = parsedMessage[len(parsedMessage) - 1]
        numberOfMessages = int(re.search(r'\d+', parsedMessage).group())
    except Exception as ex:
        print('-----------------------------------------------------------------------------')
        print('Exception caught in getNumOfMsgs')
        print(str(ex))
        print('-----------------------------------------------------------------------------\n')
    
    return numberOfMessages

#########################################################################################################
# Retrieves specific message provided the Discord message URL

async def fetchMessage(channel, url):
    parsedMessage = url.split('/')

    # Message id will be the last param in Discord URL
    messageId = int(parsedMessage[len(parsedMessage) - 1])

    print('-----------------------------------------------------------------------------')
    print('Fetching Message')
    print('Channel Name: ' + channel.name)
    print('\nMessage URL: ' + url)
    print('\nMessage ID: ' + str(messageId))
    print('-----------------------------------------------------------------------------\n')

    fetchedMessage = await channel.fetch_message(messageId)

    print('-----------------------------------------------------------------------------')
    print('Message Fetched')
    print('Author: ' + fetchedMessage.author.display_name)
    print('\nMessage:\n' + fetchedMessage.content)
    print('-----------------------------------------------------------------------------\n')

    return fetchedMessage

#########################################################################################################
# Retrieves the channel message history (Limited number of messages to lower sizes)

async def getMessageHistory(channel, msgLimit):
    print('-----------------------------------------------------------------------------')
    print('Retrieving Message History')
    print('Channel Name: ' + channel.name)
    print('\nMessage History Limit:\n' + str(msgLimit))
    print('-----------------------------------------------------------------------------\n')
    return await channel.history(limit=msgLimit).flatten()

#########################################################################################################
# Filters the message history for the target user

def filterMessageHistory(messages, user, msgLimit):
    filteredMessages = [msg for msg in messages if msg.author == user]
    filteredMessages = filteredMessages[0:msgLimit]

    return filteredMessages

#########################################################################################################
# Send message out to desired channel

async def sendMessage(channel, message):
    print('-----------------------------------------------------------------------------')
    print('Sending Message')
    print('Channel Name: ' + channel.name)
    print('\nMessage:\n' + message)
    print('-----------------------------------------------------------------------------\n')
    await channel.send(message)

#########################################################################################################
# Delete desired message

async def deleteMessage(message):
    print('-----------------------------------------------------------------------------')
    print('Deleting Message')
    print('Author: ' + message.author.display_name)
    print('\nMessage:\n' + message.clean_content)
    print('-----------------------------------------------------------------------------\n')
    await message.delete()
    
#########################################################################################################
# On_message handler - Executes after message is detected

@client.event
async def on_message(message):
    spaceDelimMessage = message.content.split(' ')

    # Message isn't from mock bot and message includes !mock
    if (client.user != message.author) and (spaceDelimMessage[0] == MOCK_TRIGGER):
        await deleteMessage(message)
        msgWithoutTrg = message.content.replace('!mock ', '')

        # Prompts user to provide command if not provided
        if len(spaceDelimMessage) <= 1:
            await sendMessage(message.channel, 'Please provide a command\nUse ***!mock help*** for a help menu')

        # Help menu
        elif spaceDelimMessage[1] == 'help':
            await sendMessage(message.channel, HELP_MENU)

        # Mock a specific message
        elif ('https://discordapp.com/channels' in spaceDelimMessage[1]):
            fetchedMessage = await fetchMessage(message.channel, spaceDelimMessage[1])
            mockedMessage = MoCk(fetchedMessage.content)
            await sendMessage(message.channel, mockedMessage)
        
        # Mock x number of messages of target user
        elif len(message.mentions) > 0:
            targetUser = message.mentions[0]
            numOfMessages = await getNumOfMsgs(message.channel, msgWithoutTrg)
            
            if numOfMessages > 10:
                await sendMessage(message.channel, 'MoCk BoT can only mock 10 messages or less at a time')
            else:
                messageHistory = await getMessageHistory(message.channel, 1000)

                if numOfMessages == -1:
                    filterMessages = filterMessageHistory(messageHistory, targetUser, 1)
                else:
                    filterMessages = filterMessageHistory(messageHistory, targetUser, numOfMessages)

                for msg in filterMessages:
                    mockedMessage = MoCk(msg.content)
                    await sendMessage(message.channel, targetUser.mention + ' ' + mockedMessage)
        
        # Mock provided message
        else:
            mockedMessage = MoCk(msgWithoutTrg)
            await sendMessage(message.channel, mockedMessage)

#########################################################################################################
# On_ready handler - Executes after bot starts up

@client.event
async def on_ready():
    print(f'{client.user} has connected')

#########################################################################################################
# Startup command to start the bot

client.run(BOT_TOKEN)