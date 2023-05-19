import discord
import discord.ext.commands as commands
import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from cogs.gamble_cog import GambleCog



@pytest_asyncio.fixture
async def bot():
    test_bot = commands.Bot(command_prefix='$', intents=discord.Intents.all(), help_command=None)
    await test_bot._async_setup_hook()  # setup the loop
    await test_bot.add_cog(GambleCog(test_bot))  
    dpytest.configure(test_bot)
    return test_bot


@pytest.mark.asyncio
async def test_my_cog(bot):

    message = (f'$ping Ping')
    await dpytest.message(message)
    assert dpytest.verify().message().contains().content('Pong!')
