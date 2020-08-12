import re
import discord

##########################################################################################
# Global definitions

tokenFile = open('.env', 'r')
helpMenuFile = open('help_menu.txt', 'r')

BOT_TOKEN = tokenFile.read()
HELP_MENU = helpMenuFile.read()

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

    # Message tags mock bot and message isn't from mock bot
    if (client.user in message.mentions) and (client.user != message.author):
        # Help menu
        if 'help' in message.content:
            await message.channel.send(HELP_MENU)
        
        # Mock x number of messages of target user
        elif len(message.mentions) > 1:
            numMessages = 0

            try:
                parsedMessage = message.content.split('>')
                parsedMessage = parsedMessage[len(parsedMessage) - 1]
                numMessages = int(re.search(r'\d+', parsedMessage).group())
            except:
                print('No target number found in Discord message')
            
            if numMessages > 10:
                await message.channel.send('MoCk BoT can only mock 10 messages or less at a time')
            elif numMessages != 0:
                targetUser = message.mentions[1]
                messages = await message.channel.history(limit=1000).flatten()

                filter(lambda x: x.author == targetUser, messages)
                messages = messages[0:numMessages]

                for msg in messages:
                    mockedMessage = MoCk(msg.content)
                    await message.channel.send(mockedMessage)
        
        # Mock provided message
        else:
            mockedMessage = MoCk(message.content)
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