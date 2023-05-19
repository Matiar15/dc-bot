import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from discord.ext import commands
from gamble_cog import GambleCog


test_bot = commands.Bot(command_prefix='$')

test_bot.add_cog(GambleCog(test_bot))

@pytest.mark.asyncio
async def test_my_cog():
    # Inicjalizacja środowiska testowego
    dpytest.configure(test_bot)

    # Wywołanie konkretnej komendy w cogu
    message = (f'$toss 300')
    await dpytest.message(message)

    # Asercje na podstawie oczekiwanych wyników
    response = await dpytest.sent_queue.get()
    assert response.content == 'I couldn\'t find your balance, consider adding one! 😑'
