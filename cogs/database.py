import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection


class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(description='Dodaj się do bazy danych')
    async def addtodatabase(self, interaction: discord.Interaction): 
        
        '''This command first gets query and if the data is None returns an Error, because user is already in the database. After this it injects data to the database.''' 

        author = interaction.user
        author_str = str(author)
        values = (author_str,)

        query = ('SELECT user_name FROM discord_user where user_name = %s')

        try:
            if mysqlconnection.mysqlQueryWithValue(query, values) is None: raise mysqlconnection.IntegrityError() # checks if a user has already given the cridentials to the db
        except mysqlconnection.IntegrityError:
            await interaction.response.send_message('You\'ve already been added to the database, don\'t waste my time 😤😤') 
        else:    
            query = ('INSERT INTO discord_user_balance (balance_amount) VALUES (1000)')

        try:
            balance_id = mysqlconnection.mysqlInsert(query)
        except mysqlconnection.Error:
            await interaction.response.send_message('Something went bad with adding your balance, call the ambulance(or maybe a bot owner)! 🚑🚑')
        
        balance_id = str(balance_id)
        values_with_balance = (author_str, balance_id)
        query = ('INSERT INTO discord_user (user_name, balance_id) VALUES (%s, %s)')
        try:    
            
            mysqlconnection.mysqlInsertWithValue(query, values_with_balance)
        except mysqlconnection.Error:
            await interaction.response.send_message('Something went bad with adding you to the database 😥')
        else:
            await interaction.response.send_message(str(author) + ' has been added to the database 😘😘😘')

     
    @app_commands.command(description='Usuń się z bazy danych (ale jak to zrobisz to będzie mi smutno 🤔🤔)')
    async def deletefromdatabase(self, interaction: discord.Interaction):
        
        '''Deletes user from database if exisits.'''
        
        author = interaction.user
        
        author_str = str(author)
        values = (author_str,)

        query = (""" DELETE FROM discord_user, discord_user_balance
                     USING discord_user
                     INNER JOIN discord_user_balance
                     WHERE discord_user.user_name = %s
                         AND discord_user.balance_id = discord_user_balance.balance_id
                     """)
        try:
            mysqlconnection.mysqlQueryDeleteUpdateWithValue(query, values)
        except mysqlconnection.Error:
            await interaction.response.send_message('Maybe you haven\'t made an account, consider adding yourself to the database 😘')
        finally:
            await interaction.response.send_message('You were successfully deleted from the database 🤣🤣🤣')
        

async def setup(bot):
    await bot.add_cog(database(bot))

