import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection
import random
import asyncio


class gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        
    #FIXME: get redundant code from functions and pass it to another common function
    #TODO: add roulette function <- in progress!
    #TODO: add blackjack function
    #TODO: add slots function
   

    @app_commands.command()
    @app_commands.choices(choice=[app_commands.Choice(name="Tails", value="tails"),
                                    app_commands.Choice(name="Heads", value="heads")])
    async def toss(self, interaction: discord.Interaction, amount: int , choice: app_commands.Choice[str]):
        '''Toss a coin. If you win, you get 2x coins you have passed to command arg and if you lose, your balance is shortened by the number you put to the amount arg.'''
        await interaction.response.defer()
        author = interaction.user
        author : str = str(author)
        
        values: tuple = (author,)
        
        query = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id 
            FROM discord_user_balance 
            join discord_user 
            on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data : tuple = mysqlconnection.mysqlQueryWithValue(query, values)
            balance : int = data[0][0]
            if amount > balance: 
                raise ValueError
            balance -= amount
            
        except mysqlconnection.Error:
            await interaction.followup.send(f'Something went wrong with executing your request 😣')
            
        except ValueError:
            await interaction.followup.send(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐')
            
        else: 
            await interaction.followup.send(f'Tossing...')
            await asyncio.sleep(1)
            
            toss_a_coin = random.choice(['heads', 'tails'])
            await interaction.followup.send(f'I tossed {toss_a_coin}!')
            
            if toss_a_coin == choice.value:
                await asyncio.sleep(1)
                await interaction.followup.send('You won! 👏👏')
                amount *= 2
                balance += amount
            
            else:
                await asyncio.sleep(1)
                await interaction.followup.send('Unfortunately, you lost. Maybe try again! 🙄')
            
            query = ("""UPDATE discord_user_balance
                    SET balance_amount = %s
                    WHERE balance_id = %s""")
            values = (balance, data[0][1])
            mysqlconnection.mysqlUpdateWithValue(query, values)
            
            await asyncio.sleep(2)
            await interaction.followup.send(f'Your current balance is {balance} 🧔')
           
            
    @app_commands.command()
    @app_commands.choices(color=[app_commands.Choice(name="Black", value="black"),
                                    app_commands.Choice(name="Red", value="red"),
                                    app_commands.Choice(name="Green", value="green")])
    async def roulette(self, interaction: discord.Interaction, amount: int , color: app_commands.Choice[str]):
        author = interaction.user
        author : str = str(author)
        
        values: tuple = (author,)
        
        query = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id 
            FROM discord_user_balance 
            join discord_user 
            on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        try:
            data : tuple = mysqlconnection.mysqlQueryWithValue(query, values)
            balance : int = data[0][0]
            if amount > balance: 
                raise ValueError
            balance -= amount
            
        except mysqlconnection.Error:
            await interaction.followup.send(f'Something went wrong with executing your request 😣')
            
        except ValueError:
            await interaction.followup.send(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐')      

        roll_roulette = random.choice(['black', 'green', 'red'])
                
async def setup(bot):
    await bot.add_cog(gamble(bot))

