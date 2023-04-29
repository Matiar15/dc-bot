import discord
from discord.ext import commands
from discord import app_commands

class gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    @app_commands.command()
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('test done correcly! 😎')

    

async def setup(bot):
    await bot.add_cog(gamble(bot))
