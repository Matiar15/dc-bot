import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection
from datetime import datetime


class balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(description='Sprawdź swój balance 😎😎 (najpierw dodaj się do bazy danych!)')
    async def balance(self, interaction: discord.Interaction):
            
        '''Checks if user has balance in database and if so, gives the amount of coins.'''    

        author = interaction.user
        
        author_str = str(author)
        values = (author_str,)

        query = (""" SELECT discord_user_balance.balance_amount 
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data = mysqlconnection.mysqlQueryWithValue(query, values)
        except mysqlconnection.Error:
            await interaction.response.send_message('I couldn\'t find your balance, consider adding one! 😑')
        else:    
            await interaction.response.send_message(f'Your current balance is: {data[0][0]} bucks! 💸💸💸')


    @app_commands.command(description='Codziennie otrzymujesz darmowe 500 coinsów 🤑🤑')
    async def daily(self, interaction: discord.Interaction):
        
        '''Adds 500 coins to database balance if there was 24h delay in between getting daily reward.'''
        
        author = interaction.user
        
        author_str = str(author)
        values = (author_str,)

        query = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id, daily_reward_at
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data = mysqlconnection.mysqlQueryWithValue(query, values)
        except mysqlconnection.Error as e:
            await interaction.response.send_message(f'I couldn\'t find your balance, consider adding one! 😑 -> Error type: {e}')
        else: 
            db_date = data[0][2]
            
            balance_amount = data[0][0]
            balance_amount += 500
            
            curr_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S')
            curr_date_obj = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')
            
            if db_date == None:

                query = """UPDATE discord_user_balance
                        SET balance_amount = %s, daily_reward_at = %s
                        WHERE balance_id = %s"""
                values = (balance_amount, curr_time, data[0][1])
                
                try:
                    mysqlconnection.mysqlUpdateWithValue(query, values)
                except mysqlconnection.Error:
                    await interaction.response.send_message(f'Something went wrong with inserting your daily money 😑')
                else:
                    await interaction.response.send_message(f'Daily inserted correctly! Your current balance is: {balance_amount} 😁')
            else:
                date_diff = curr_date_obj - db_date
                if (date_diff.total_seconds()) > 86400:
                    query = """UPDATE discord_user_balance
                        SET balance_amount = %s, daily_reward_at = %s
                        WHERE balance_id = %s"""
                    values = (balance_amount, curr_date_obj, data[0][1])
                    
                    try:
                        mysqlconnection.mysqlUpdateWithValue(query, values)
                    except mysqlconnection.Error:
                        await interaction.response.send_message(f'Something went wrong with inserting your daily money 😑')
                    else:
                        await interaction.response.send_message(f'Daily inserted correctly! Your current balance is: {balance_amount} 😁')
                else:
                    await interaction.response.send_message(f'Your last daily reward was collected at: {db_date}, so you have to wait!')
                

async def setup(bot):
    await bot.add_cog(balance(bot))