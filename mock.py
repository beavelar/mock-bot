import re
import discord

##########################################################################################
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

##########################################################################################
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

##########################################################################################
# On_message handler - Executes after message is detected

@client.event
async def on_message(message):
    # TODO: Implement ability to mock specific messages provided a message link
    #content = message.content[message.content.find('>') + 2:]
    #if ('https://discordapp.com/channels' in content):
        #msgId = int(content.split('/')[5])
        #fetchedMessage = await message.channel.fetch_message(msgId)

    spaceDelimMessage = message.content.split(' ')

    # Message isn't from mock bot and message includes !mock
    if (client.user != message.author) and (spaceDelimMessage[0] == MOCK_TRIGGER):
        msgOnly = message.content.replace('!mock ', '')

        # Prompts user to provide command if not provided
        if len(spaceDelimMessage) <= 1:
            await message.channel.send('Please provide a command\nUse ***!mock help*** for a help menu')

        # Help menu
        elif spaceDelimMessage[1] == 'help':
            await message.channel.send(HELP_MENU)
        
        # Mock x number of messages of target user
        elif len(message.mentions) > 0:
            numMessages = 0
            
            try:
                parsedMessage = msgOnly.split('>')
                parsedMessage = parsedMessage[len(parsedMessage) - 1]
                numMessages = int(re.search(r'\d+', parsedMessage).group())
            except:
                await message.channel.send('No target number found in Discord message')
            
            if numMessages > 10:
                await message.channel.send('MoCk BoT can only mock 10 messages or less at a time')
            elif numMessages != 0:
                targetUser = message.mentions[0]
                messages = await message.channel.history(limit=1000).flatten()

                filter(lambda x: x.author == targetUser, messages)
                messages = messages[0:numMessages]

                for msg in messages:
                    mockedMessage = MoCk(msg.content)
                    await message.channel.send(mockedMessage)
        
        # Mock provided message
        else:
            mockedMessage = MoCk(msgOnly)
            await message.channel.send(mockedMessage)
        
        await message.delete()

##########################################################################################
# On_ready handler - Executes after bot starts up

@client.event
async def on_ready():
    print(f'{client.user} has connected')

##########################################################################################
# Startup command to start the bot

client.run(BOT_TOKEN)