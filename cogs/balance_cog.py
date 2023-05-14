import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import mysqlconnection
import cog_helper


class BalanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(description='Check your balance 😎😎 (First off add yourself to database!)')
    async def balance(self, interaction: discord.Interaction): 
        r'''Checks if user has balance in database and if so, gives the amount of coins.

            Raises
            -----------
            mysqlconnection.Error
                User was not added to the MySQL database or something went wrong with database connection.
            TypeError
                Data read by MySQL query was None.
        '''    
        author: discord.User | discord.Member = interaction.user
        
        author: tuple[str] = cog_helper.user_to_str(author)
        

        query: str = (""" SELECT discord_user_balance.balance_amount 
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data: list = mysqlconnection.mysql_query_with_value(query, author)
            if data is None: raise TypeError 
        
        except TypeError as _:
            await interaction.response.send_message(f'I couldn\'t find your balance, consider adding one! 😑')
        
        except mysqlconnection.Error as _:
            await interaction.response.send_message('Something went wrong with database connection 😑')
        
        else:    
            await interaction.response.send_message(f'Your current balance is: {data[0]} bucks! 💸💸💸')


    @app_commands.command(description='Everyday you get 500 coins!🤑🤑')
    async def daily(self, interaction: discord.Interaction):
        r'''Adds 500 coins to database balance if there was 24h delay in between getting daily reward.
            
            Raises
            -----------
            mysqlconnection.Error
                User was not added to the MySQL database or something went wrong with database connection.
            TypeError
                Data read by MySQL query was None.
        '''
        author: discord.User | discord.Member = interaction.user
        
        author: tuple[str] = cog_helper.user_to_str(author)

        query: str = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id, daily_reward_at
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data: list = mysqlconnection.mysql_query_with_value(query, author)
            if data is None: raise TypeError
        
        except TypeError as _:
            await interaction.response.send_message(f'I couldn\'t find your balance, consider adding one! 😑')

        except mysqlconnection.Error as _:
                    await interaction.response.send_message(f'Something went wrong with database connection 😑')    
        
        else: 
            daily_reward: datetime = data[2]               # Getting the data from MySQL query into variables.
            balance_id: int = data[1]                    
            balance_amount: int = data[0]
            balance_amount += 500
            
            curr_time: str = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S') # Getting current time and changing it 
            curr_time: datetime = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')         #     into datetime object.
            
            if daily_reward == None:

                try:
                    update_balance(balance_amount, curr_time, balance_id)
                
                except mysqlconnection.Error as _:
                    await interaction.response.send_message(f'Something went wrong with inserting your daily money 😑')
                
                else:
                    await interaction.response.send_message(f'Daily inserted correctly! Your current balance is: {balance_amount} 😁')
            
            else:
                date_diff: datetime = curr_time - daily_reward
                
                if (date_diff.total_seconds()) > 86400:
                    try:
                        update_balance(balance_amount, curr_time, balance_id)
                    
                    except mysqlconnection.Error as _:
                        await interaction.response.send_message(f'Something went wrong with inserting your daily money 😑')
                    
                    else:
                        await interaction.response.send_message(f'Daily inserted correctly! Your current balance is: {balance_amount} 😁')
                
                else:
                    await interaction.response.send_message(f'Your last daily reward was collected at: {daily_reward}, so you have to wait!')
                

def update_balance(balance_amount: int, daily_collected_at: datetime, balance_id: int):
    r'''Updates balance and changes daily_reward_at timestamp in MySQL database.
    
        Parameters
        -----------
        balance_amount: :class:`int`
            Amount of user's balance.
        daily_reward_at: :class:`datetime`
            MySQL timestamp, last time user has collected daily reward.
        balance_id: :class:`int`
            ID of user's balance.
            
        Raises
        -----------
        mysqlconnection.Error
            Something went wrong with database connection.  
    '''
    query: str = """UPDATE discord_user_balance
                        SET balance_amount = %s, daily_reward_at = %s
                        WHERE balance_id = %s"""
    values: tuple = (balance_amount, daily_collected_at, balance_id)
    mysqlconnection.mysql_query_delete_update_with_value(query, values)


async def setup(bot):
    await bot.add_cog(BalanceCog(bot))
    