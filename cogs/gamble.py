import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection
import random


conn = mysqlconnection.mysqlConnection()

class gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    

    @app_commands.command()
    @app_commands.choices(choice=[app_commands.Choice(name="Tails", value="tails"),
                                    app_commands.Choice(name="Heads", value="heads")])
    async def toss(self, interaction: discord.Interaction, amount: int , choice: app_commands.Choice[str]):
        '''Toss a coin, gets coins from database returns them to database.'''
        
        
        author = interaction.user
        author_str = str(author)
        
        conn = mysqlconnection.mysqlConnection()
        
        values = (author_str,)
        
        query = (""" SELECT discord_user_balance.balance_amount 
            FROM discord_user_balance 
            join discord_user 
            on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        try:
            balance = mysqlconnection.mysqlQuery(conn, query, values)

            await interaction.response.send_message(f'{amount}, {balance}')
            if amount > balance: raise ValueError
            balance -= amount
        except mysqlconnection.Error as e:
            await interaction.response.send_message(f'Something went wrong with executing your request 😣 (Error {e})')
        except ValueError as ve:
            await interaction.response.send_message(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐 (Error : {ve})')
        else: 
            toss_a_coin = random.choice(['heads', 'tails'])
            await interaction.response.send_message(f'I tossed a {toss_a_coin}!')
            if toss_a_coin == choice.value:
                await interaction.followup.send('You won! 👏👏')
                amount *= 2
                balance += amount
            else:
                await interaction.followup.send('Unfortunetly, you lost. Maybe try again! 🙄')
        
            query = (""" UPDATE discord_user_balance.balance_amount 
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
            
            mysqlconnection.mysqlUpdateWithValue(conn, query, values)
            await interaction.response.send_message(f'Your current balance is {balance} 🧔')
                
                
                
        
    

async def setup(bot):
    await bot.add_cog(gamble(bot))


def getBalanceFromDatabase(author: str):
    conn_response = mysqlconnection.checkConnection(conn)
    author_str = str(author)
    values = (author_str,)
    query = (""" SELECT discord_user_balance.balance_amount 
            FROM discord_user_balance 
            join discord_user 
            on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
    return (conn_response, query, values)

def returnBalanceToDatabase(author: str):
    conn_response = mysqlconnection.checkConnection(conn)
    author_str = str(author)
    values = (author_str,)
    query = (""" UPDATE discord_user_balance.balance_amount 
            FROM discord_user_balance 
            join discord_user 
            on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
    return (conn_response, query, values)