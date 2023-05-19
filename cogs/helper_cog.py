import discord
from discord.ext import commands
from discord import app_commands
import os


directory = os.getcwd().replace('\\', '/')

class CogHelper(commands.Cog):
    r'''A cog that is for handling more information about commands.'''
    def __init__(self, bot):
        self.bot = bot
       
       
    @app_commands.command(description="Help 🙄🙄")
    @app_commands.choices(category=[app_commands.Choice(name="Gambling", value="gambling"),
                                    app_commands.Choice(name="Database", value="database"),
                                    app_commands.Choice(name="Balance", value="balance"),
                                    app_commands.Choice(name="Reddit", value="reddit")])
    async def help(self, interaction: discord.Interaction, category: app_commands.Choice[str]):
        file = discord.File(f"{directory}/resources/matbotpic.png", filename="matbotpic.png")
        match category.value:
            case 'gambling':
                embed = discord.Embed(title='Gambling', description='MatBot\'s gambling commands.', colour=0x992d22)
                
                embed.set_thumbnail(url='attachment://matbotpic.png')
                embed.add_field(name='/toss', value='''Toss a coin.
                    The amount you put into command will be taken from your database balance.
                    If your guess was right, you get the amount back doubled.''')
                embed.add_field(name='/roulette', value='''Choose a color.
                    You have color choices of: Black, Red, Green, Blackfish, Redfish.
                    Black/Red multiplies amount by 2 times.
                    Green multiplies amount by 14 times.
                    Fish multiplies amount by 7 or by 2 if color of the fish was correct.''', inline=False)
                embed.add_field(name='/wordle', value='''Play a wordle game with bot.
                    :regional_indicator_s: stands for a letter that was correct and it\'s in a perfect position.
                    'S' letter stands for a letter that is in the word but on a wrong position.
                    's' letter stands for a letter that is not i the word.
                    Words are 5 letter, if you get the word on the first try, you get 2x of the amount.
                    You have 6 tries, each try you lose 0.2 from your amount.''')
                
                embed.set_footer(text=f'Information requested by: {str(interaction.user)}')
                await interaction.response.send_message(file=file, embed=embed)
            
            case 'database':
                
                embed = discord.Embed(title='Database', description='MatBot\'s database commands.', colour=0xad1457)
                embed.set_thumbnail(url='attachment://matbotpic.png')
                
                embed.add_field(name='/addtodatabase', value='''Add yourself to database.
                    You are adding yourself to database to enable gambling, make your profile.
                    Later on you can add your League of Legends PUUID to receive information about your recent matches.''')
                embed.add_field(name='/deletefromdatabase', value='''Delete yourself from database.
                    If you are not keen on at the moment to be in a database you can delete yourself by writing this command.''', inline=False)
                
                embed.set_footer(text=f'Information requested by: {str(interaction.user)}')
                
                await interaction.response.send_message(file=file, embed=embed)
            
            case 'balance':
                
                embed = discord.Embed(title='Balance', description='MatBot\'s balance commands.', colour=0x1f8b4c)
                
                embed.set_thumbnail(url='attachment://matbotpic.png')
                embed.add_field(name='/balance', value='''Check your balance.
                    You can check the amount of coins you have on yourself.''')
                embed.add_field(name='/daily', value='''Get daily reward of 500 coins.
                    You can collect this reward daily. It is exacly 24 hours after previous collection.''', inline=False)
                
                embed.set_footer(text=f'Information requested by: {str(interaction.user)}')
                
                await interaction.response.send_message(file=file, embed=embed)
            
            case 'reddit':
                embed = discord.Embed(title='Reddit', description='MatBot\'s reddit commands.', colour=0xe74c3c)
                embed.set_thumbnail(url='attachment://matbotpic.png')
                
                embed.add_field(name='/meme', value='Shows a meme.')
                embed.set_footer(text=f'Information requested by: {str(interaction.user)}')
                 
                await interaction.response.send_message(file=file, embed=embed)
                                 

async def setup(bot):
    await bot.add_cog(CogHelper(bot))
    