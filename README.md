# MoCk-BoT
This repository contains code for a Discord version of the Slack "mock" bot.

The goal of the bot is to "mock" the messages of target users in the Discord environment.

## Quick Links:
- [Project Requirements](#project-requirements)
- [Bot Permission Requirements](#bot-permission-requirements)
- [Stand-Alone Project Setup](#stand-alone-project-setup)

----------------------------------

## Project Requirements
- Python
  - [Python Organization Website](https://www.python.org/)
- Discord library
  - [Discord.py Installation Guide](https://discordpy.readthedocs.io/en/latest/intro.html)

## Bot Permission Requirements
The following are permission requirements needed by the MoCk BoT
 - **General Permissions**
   - View Channels
 - **Text Permissions**
   - Send Messages
   - Manage Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Mention everyone
   - Use External Emojis
   
## Stand-Alone Project Setup
- Clone the repository
- Create Discord bot account
  - [Creating a Bot Account Guide](https://discordpy.readthedocs.io/en/latest/discord.html#)
- Invite Discord bot into your Discord server with proper permissions
  - [Inviting Your Bot Guide](https://discordpy.readthedocs.io/en/latest/discord.html#inviting-your-bot)
  - View [Bot Permission Requirements](#bot-permission-requirements) for the required permissions  
- After cloning the repository, you should have a **MoCk-BoT** directory, navigate to **MoCk-BoT/environment** and create an empty .env file
  - This will contain our bot secret token
- Retrieve bot secret token
  - In Discord developer page, navigate to "Bot"
  
    ![Discord Bot Selection](/images/bot-selection-snap.PNG)
  - Under "Token", reveal token by clicking on the "Click to Reveal Token" link

    ![Token Reveal](/images/token-reveal-snap.PNG)
- Copy and paste bot token into .env file and save
- Open a command line window of choice
  - Command prompt, GitBash, etc.
- Navigate to the project base directory
- Execute the following command to spin up the bot:
  - *python mock.py*
- View Discord server
  - MoCk Bot should now appear as online and listening to channel messages