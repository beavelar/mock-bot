import discord

tokenFile = open(".env", "r")
BOT_TOKEN = tokenFile.read()
client = discord.Client()

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

@client.event
async def on_message(message):
    if (client.user in message.mentions) and (client.user != message.author):
        mockedMessage = MoCk(message.content)
        await message.channel.send(mockedMessage)

@client.event
async def on_ready():
    print(f'{client.user} has connected')

client.run(BOT_TOKEN)