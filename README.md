# MoCk-BoT
Discord bot replicate of the Slack "mock" bot.

----------------------------------

## Bot Permission Requirements
The following are permission requirements of the MoCk BoT
 - **General Permissions**
   - View Channels
 - **Text Permissions**
   - Send Messages
   - Read Message History
   - Use External Emojis

## Requirements
*Project can be built/ran with Docker or docker-compose view the steps to setup and run the project with [Docker](#setup-and-run-with-docker) or [docker-compose](#setup-and-run-with-docker-compose)*
- Python
   
## Register and Invite Discord Bot
- Create Discord bot account
  - [Creating a Bot Account Guide](https://discordpy.readthedocs.io/en/latest/discord.html#)
- Invite Discord bot into your Discord server with proper permissions
  - [Inviting Your Bot Guide](https://discordpy.readthedocs.io/en/latest/discord.html#inviting-your-bot)
  - View [Bot Permission Requirements](#bot-permission-requirements) for the required permissions  

## Setup Environment
- Create a .env file. Utilize the .env.template file as a template
- Set the **BOT_TOKEN** value to your bot token
  - In Discord developer page, navigate to "Bot"
  
    ![Discord Bot Selection](/images/bot-selection-snap.PNG)
  - Under "Token", reveal token by clicking on the "Click to Reveal Token" link

    ![Token Reveal](/images/token-reveal-snap.PNG)

## Setup and Run with Python
- Install the Python dependencies
  - **pip install -r requirements.txt**
- Run the discord bot
  - ****
## Setup and Run with Docker
- Build the docker image
  - **docker build -t mock-bot .**
- Run the build docker image
  - **docker run mock-bot**

## Setup and Run with docker-compose
- Build and run the docker images
  - **docker-compose up --build -d**

## Usage
- To mock the previous message
  - *!mock*