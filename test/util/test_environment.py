import os

from src.util.environment import environment


def test_init_environment():
    bot_token = "Bot Token"
    bot_trigger = "Bot Trigger"

    os.environ["BOT_TOKEN"] = bot_token
    os.environ["BOT_TRIGGER"] = bot_trigger

    env = environment()
    assert env.bot_token is bot_token
    assert env.bot_trigger is bot_trigger
