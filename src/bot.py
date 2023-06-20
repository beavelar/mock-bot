import logging

from discord import Guild, Intents
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import CommandError, CommandNotFound
from util.environment import environment
from util.mock import mock

logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(name)s.%(funcName)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

env = environment()
intents = Intents(guilds=True, message_content=True, messages=True)
bot = Bot(command_prefix="!", intents=intents)


@bot.command(name=env.bot_trigger)
async def mock_message(ctx: Context):
    """
    Captures any command messages received from the discord client. Mocks the first
    messages that isn't from the client or from the user of the command and sends the
    message to the same discord channel
    """
    async for message in ctx.channel.history(limit=100):
        if message.author != ctx.author and message.author != bot.user:
            await ctx.channel.send(mock(message.content))
            break


@bot.event
async def on_command_error(__ctx__: Context, error: CommandError):
    """
    Captures any command errors raised by the discord client
    """
    if not isinstance(error, CommandNotFound):
        logger.error(f"Unhandled error occurred in on_command_error: {error}")


@bot.event
async def on_guild_join(guild: Guild):
    """
    Captures on_guild_join event
    """
    logger.info(f"{bot.user} has joined a guild: {guild.name}")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected")


bot.run(env.bot_token)
