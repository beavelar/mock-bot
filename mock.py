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
#
# Parameters
# message: string
#
# Returns: string

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
#
# Parameters
# channel: Channel (Discord API)
# message: string
#
# Returns: integer

async def getNumOfMsgs(channel, message):
    numberOfMessages = -1

    try:
        parsedMessage = message.split('>')
        parsedMessage = parsedMessage[len(parsedMessage) - 1]
        numberOfMessages = re.search(r'\d+', parsedMessage)
        
        if numberOfMessages is None:
            numberOfMessages = -1
        else:
            numberOfMessages = int(re.search(r'\d+', parsedMessage).group())
    except Exception as ex:
        print('-----------------------------------------------------------------------------')
        print('Exception caught in getNumOfMsgs')
        print(str(ex))
        print('-----------------------------------------------------------------------------\n')
    
    return numberOfMessages

#########################################################################################################
# Retrieves specific message provided the Discord message URL
#
# Parameters
# channel: Channel (Discord API)
# url: string
#
# Returns: None or string

async def fetchMessage(channel, url):
    fetchMessage = None
    parsedMessage = url.split('/')

    # Message id will be the last param in Discord URL
    messageId = int(parsedMessage[len(parsedMessage) - 1])

    print('-----------------------------------------------------------------------------')
    print('Fetching Message')
    print('Channel Name: ' + channel.name)
    print('\nMessage URL: ' + url)
    print('\nMessage ID: ' + str(messageId))
    print('-----------------------------------------------------------------------------\n')

    try:
        fetchedMessage = await channel.fetch_message(messageId)
        
        print('-----------------------------------------------------------------------------')
        print('Message Fetched')
        print('Author: ' + fetchedMessage.author.display_name)
        print('\nMessage:\n' + fetchedMessage.content)
        print('-----------------------------------------------------------------------------\n')
    except NotFound as ex:
        print('-----------------------------------------------------------------------------')
        print('NotFound exception caught in fetchMessage')
        print('The specified message was not found')
        print('Channel Name: ' + channel.name)
        print('\nMessage URL: ' + url)
        print('\nMessage ID: ' + str(messageId))
        print('-----------------------------------------------------------------------------\n')
    except Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in fetchMessage')
        print(client.user.display_name + ' does not have the correct permissions to retrieve the message')
        print('Channel Name: ' + channel.name)
        print('\nMessage URL: ' + url)
        print('\nMessage ID: ' + str(messageId))
        print('-----------------------------------------------------------------------------\n')
    except HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in fetchMessage')
        print('Discord fetch_message function failed to retrieve message')
        print('Channel Name: ' + channel.name)
        print('\nMessage URL: ' + url)
        print('\nMessage ID: ' + str(messageId))
        print('-----------------------------------------------------------------------------\n')

    return fetchedMessage

#########################################################################################################
# Retrieves the channel message history (Limited number of messages to lower sizes)
#
# Parameters
# channel: Channel (Discord API)
# msgLimit: integer
#
# Returns: None or List of Message (Discord API)

async def getMessageHistory(channel, msgLimit):
    messageHistory = None

    print('-----------------------------------------------------------------------------')
    print('Retrieving Message History')
    print('Channel Name: ' + channel.name)
    print('\nMessage History Limit: ' + str(msgLimit))
    print('-----------------------------------------------------------------------------\n')
    
    try:
        messageHistory = await channel.history(limit=msgLimit).flatten()
    except Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in getMessageHistory')
        print(client.user.display_name + ' does not have the correct permissions to retrieve the message')
        print('Channel Name: ' + channel.name)
        print('-----------------------------------------------------------------------------\n')
    except HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in getMessageHistory')
        print('Discord history function failed to retrieve message history')
        print('Channel Name: ' + channel.name)
        print('-----------------------------------------------------------------------------\n')

    return messageHistory

#########################################################################################################
# Filters the message history for the target user
#
# Parameters
# channel: Channel (Discord API)
# msgLimit: integer
#
# Returns: None or List of Message (Discord API)

def filterMessageHistory(messages, user, msgLimit):
    filteredMessages = [msg for msg in messages if msg.author == user]
    filteredMessages = filteredMessages[0:msgLimit]

    return filteredMessages

#########################################################################################################
# Send message out to desired channel
#
# Parameters
# channel: Channel (Discord API)
# message: string

async def sendMessage(channel, message):
    print('-----------------------------------------------------------------------------')
    print('Sending Message')
    print('Channel Name: ' + channel.name)
    print('\nMessage:\n' + message)
    print('-----------------------------------------------------------------------------\n')
    
    try:
        await channel.send(message)
    except HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in sendMessage')
        print('Discord send function failed to send message')
        print('Channel Name: ' + channel.name)
        print('\nMessage:\n' + message)
        print('-----------------------------------------------------------------------------\n')
    except Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in sendMessage')
        print(client.user.display_name + ' does not have the correct permissions to retrieve the message')
        print('Channel Name: ' + channel.name)
        print('\nMessage:\n' + message)
        print('-----------------------------------------------------------------------------\n')    

#########################################################################################################
# Delete desired message
#
# Parameters
# message: Message (Discord API)

async def deleteMessage(message):
    print('-----------------------------------------------------------------------------')
    print('Deleting Message')
    print('Author: ' + message.author.display_name)
    print('\nMessage:\n' + message.clean_content)
    print('-----------------------------------------------------------------------------\n')

    try:
        await message.delete()
    except HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in deleteMessage')
        print('Discord delete function failed to delete desired message')
        print('Author: ' + message.author.display_name)
        print('\nMessage:\n' + message.clean_content)
        print('-----------------------------------------------------------------------------\n')
    
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
            await sendMessage(message.channel, 'Please provide a command\nUse ***!mock help*** for a help menu')

        # Help menu
        elif spaceDelimMessage[1] == 'help':
            await sendMessage(message.channel, HELP_MENU)

        # Mock a specific message
        elif ('https://discordapp.com/channels' in spaceDelimMessage[1]):
            fetchedMessage = await fetchMessage(message.channel, spaceDelimMessage[1])
            
            if fetchedMessage is not None:
                mockedMessage = MoCk(fetchedMessage.content)
                await sendMessage(message.channel, mockedMessage)
            else:
                await sendMessage(message.channel, 'Failed to mock targeted message')
        
        # Mock x number of messages of target user
        elif len(message.mentions) > 0:
            targetUser = message.mentions[0]
            numOfMessages = await getNumOfMsgs(message.channel, msgWithoutTrg)
            
            if numOfMessages > 10:
                await sendMessage(message.channel, 'MoCk BoT can only mock 10 messages or less at a time')
            else:
                messageHistory = await getMessageHistory(message.channel, 1000)

                if messageHistory is not None:
                    if numOfMessages == -1:
                        filterMessages = filterMessageHistory(messageHistory, targetUser, 1)
                    else:
                        filterMessages = filterMessageHistory(messageHistory, targetUser, numOfMessages)
                    
                    for msg in filterMessages:
                        mockedMessage = MoCk(msg.content)
                        await sendMessage(message.channel, targetUser.mention + ' ' + mockedMessage)
                else:
                    await sendMessage(message.channel, 'Failed to mock historical message(s)')
        
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