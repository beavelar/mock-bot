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
        if char != ' ':
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
    if (client.user in message.mentions) and (client.user != message.author):
        if ('help' in message.content):
            await message.channel.send(HELP_MENU)
        else:
            mockedMessage = MoCk(message.content)
            await message.channel.send(mockedMessage)

##########################################################################################
# On_ready handler - Executes after bot starts up

@client.event
async def on_ready():
    print(f'{client.user} has connected')

##########################################################################################
# Startup command to start the bot

client.run(BOT_TOKEN)