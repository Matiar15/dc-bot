import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection
import cog_helper


class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Add yourself to database 😁😁')
    async def addtodatabase(self, interaction: discord.Interaction):  
        r'''Adds user to the database.
        
            Raises
            -----------
            mysqlconnection.IntegrityError
                The same data was already in database. 
            mysqlconnection.Error
                Something went wrong with connection to MySQL.
        ''' 
        author: discord.User | discord.Member = interaction.user
        author: tuple[str] = cog_helper.user_to_str(author)

        query: str = ('SELECT user_name FROM discord_user where user_name = %s')
        
        try:
            data = mysqlconnection.mysql_query_with_value(query, author)
            
            if data is not None: raise mysqlconnection.IntegrityError()
                                                                # checks if a user has already given the cridentials to the db
                                                                    
        except mysqlconnection.IntegrityError() as _:
            await interaction.response.send_message('You\'ve already been added to the database, don\'t waste my time 😤😤') 
        
        except mysqlconnection.Error as _:
            await interaction.response.send_message('Something went bad with adding your balance, call the ambulance(or maybe a bot owner)! 🚑🚑')
        
        else:    
            query: str = ('INSERT INTO discord_user_balance (balance_amount) VALUES (1000)')

            try:
                balance_id: int = mysqlconnection.mysql_insert(query)
                
            except mysqlconnection.Error as _:
                await interaction.response.send_message('Something went bad with adding your balance, call the ambulance(or maybe a bot owner)! 🚑🚑')
            
            else:
                
                query: str = ('INSERT INTO discord_user (user_name, balance_id) VALUES (%s, %s)')
                values: tuple = (author[0], str(balance_id))
                
                try:    
                    _ = mysqlconnection.mysql_insert_with_value(query, values)
                    
                except mysqlconnection.Error as _:
                    await interaction.response.send_message('Something went bad with adding you to the database 😥')
                
                else:
                    await interaction.response.send_message(author[0] + ' has been added to the database 😘😘😘')

     
    @app_commands.command(description='Delete yourself from database (i\'ll be sad😣😣)')
    async def deletefromdatabase(self, interaction: discord.Interaction):
        r'''Deletes user from database if exisits.
        
            Raises
            -----------
            mysqlconnection.Error
                User was not added to the MySQL database or something went wrong with database connection.
        '''
        author: discord.User | discord.Member = interaction.user 
        author: str = cog_helper.user_to_str(author)
        query: str = (""" SELECT discord_user_balance.balance_amount 
                FROM discord_user_balance 
                join discord_user 
                on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        try:
            data: list = mysqlconnection.mysql_query_with_value(query, author)
            if data is None: raise TypeError 
        
        except TypeError as _:
            await interaction.response.send_message(f'I couldn\'t find your balance! 😑')
        
        except mysqlconnection.Error as _:
            await interaction.response.send_message('Something went wrong with database connection 😑')
        else:
            query: str = (""" DELETE FROM discord_user, discord_user_balance
                        USING discord_user
                        INNER JOIN discord_user_balance
                        WHERE discord_user.user_name = %s
                            AND discord_user.balance_id = discord_user_balance.balance_id
                        """)
            
            try:
                mysqlconnection.mysql_query_delete_update_with_value(query, author)
            
            except mysqlconnection.Error as _:
                await interaction.response.send_message('Maybe you haven\'t made an account, consider adding yourself to the database 😘')
            
            else:
                await interaction.response.send_message('You were successfully deleted from the database 🤣🤣🤣')
        

async def setup(bot):
    await bot.add_cog(DatabaseCog(bot))
