from discord import NotFound
from discord import Forbidden
from discord import HTTPException

#########################################################################################################
# Retrieves specific message provided the Discord message URL
#
# Parameters
# bot: User (Discord API)
# channel: Channel (Discord API)
# url: string
#
# Returns: None or string

async def fetchMessage(bot, channel, url):
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
    except discord.NotFound as ex:
        print('-----------------------------------------------------------------------------')
        print('NotFound exception caught in fetchMessage')
        print('The specified message was not found')
        print('Channel Name: ' + channel.name)
        print('\nMessage URL: ' + url)
        print('\nMessage ID: ' + str(messageId))
        print('-----------------------------------------------------------------------------\n')
    except discord.Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in fetchMessage')
        print(bot.display_name + ' does not have the correct permissions to retrieve the message')
        print('Channel Name: ' + channel.name)
        print('\nMessage URL: ' + url)
        print('\nMessage ID: ' + str(messageId))
        print('-----------------------------------------------------------------------------\n')
    except discord.HTTPException as ex:
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
# bot: User (Discord API)
# channel: Channel (Discord API)
# msgLimit: integer
#
# Returns: None or List of Message (Discord API)

async def getMessageHistory(bot, channel, msgLimit):
    messageHistory = None

    print('-----------------------------------------------------------------------------')
    print('Retrieving Message History')
    print('Channel Name: ' + channel.name)
    print('\nMessage History Limit: ' + str(msgLimit))
    print('-----------------------------------------------------------------------------\n')
    
    try:
        messageHistory = await channel.history(limit=msgLimit).flatten()
    except discord.Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in getMessageHistory')
        print(bot.display_name + ' does not have the correct permissions to retrieve the message')
        print('Channel Name: ' + channel.name)
        print('-----------------------------------------------------------------------------\n')
    except discord.HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in getMessageHistory')
        print('Discord history function failed to retrieve message history')
        print('Channel Name: ' + channel.name)
        print('-----------------------------------------------------------------------------\n')

    return messageHistory

#########################################################################################################
# Send message out to desired channel
#
# Parameters
# bot: User (Discord API)
# channel: Channel (Discord API)
# message: string

async def sendMessage(bot, channel, message):
    print('-----------------------------------------------------------------------------')
    print('Sending Message')
    print('Channel Name: ' + channel.name)
    print('\nMessage:\n' + message)
    print('-----------------------------------------------------------------------------\n')
    
    try:
        await channel.send(message)
    except discord.HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in sendMessage')
        print('Discord send function failed to send message')
        print('Channel Name: ' + channel.name)
        print('\nMessage:\n' + message)
        print('-----------------------------------------------------------------------------\n')
    except discord.Forbidden as ex:
        print('-----------------------------------------------------------------------------')
        print('Forbidden exception caught in sendMessage')
        print(bot.display_name + ' does not have the correct permissions to retrieve the message')
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
    except discord.HTTPException as ex:
        print('-----------------------------------------------------------------------------')
        print('HTTPException exception caught in deleteMessage')
        print('Discord delete function failed to delete desired message')
        print('Author: ' + message.author.display_name)
        print('\nMessage:\n' + message.clean_content)
        print('-----------------------------------------------------------------------------\n')