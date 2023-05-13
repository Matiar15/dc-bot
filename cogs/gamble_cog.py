import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import json
import mysqlconnection
import cog_helper


class GambleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
    
        
    #TODO: add blackjack function
    #TODO: add slots function
   

    @app_commands.command()
    @app_commands.choices(choice=[app_commands.Choice(name="Tails", value="tails"),
                                    app_commands.Choice(name="Heads", value="heads")])
    async def toss(self, interaction: discord.Interaction, amount: int , choice: app_commands.Choice[str]):
        r'''Toss a coin. If you win, you get 2x coins you have passed to command arg and if you lose, 
        your balance is shortened by the number you put to the amount argument.
        
        Parameters
        -----------
        amount: class:`int` 
            The amount user gives from balance to play roulette.
        choice: class:`Choice[str]` 
            The side of the coin that user chooses.
            
        Raises
        -----------
        mysqlconnection.Error
            User was not added to the MySQL database or something went wrong with database connection.
        ValueError
            User's balance was smaller than amount.
        '''
        await interaction.response.defer()
        author: discord.User | discord.Member = interaction.user
        author: tuple = cog_helper.user_to_str(author)
        
        try:   
            data: list = get_balance(author, amount)  
            balance_amount: int = data[0]
            balance_id: int = data[1]
            
        except mysqlconnection.Error as _:
            await asyncio.sleep(1)
            await interaction.followup.send(f'Something went wrong with executing your request 😣')
            
        except ValueError as _:
            await asyncio.sleep(1)
            await interaction.followup.send(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐')
        
        else: 
            await interaction.followup.send(f'Tossing...')
            await asyncio.sleep(1)
            
            toss_a_coin: str = random.choice(['heads', 'tails'])
            await interaction.followup.send(f'I tossed {toss_a_coin}!')
            
            if toss_a_coin == choice.value:
                await asyncio.sleep(1)
                await interaction.followup.send('You won! 👏👏')
                amount *= 2
                balance += amount
            
            else:
                await asyncio.sleep(1)
                await interaction.followup.send('Unfortunately, you lost. Maybe try again! 🙄')
            
            try:
                update_balance(balance_id, balance_amount)
            
            except mysqlconnection.Error as _:
                await asyncio.sleep(1)
                await interaction.followup.send(f'Something went wrong with executing your request 😣')  
            
            else:
                await asyncio.sleep(2)
                await interaction.followup.send(f'Your current balance is {balance} 🧔')
           
            
    @app_commands.command()
    @app_commands.choices(color=[app_commands.Choice(name="Black", value="black"),
                                app_commands.Choice(name="Blackfish", value="blackfish"),
                                app_commands.Choice(name="Red", value="red"),
                                app_commands.Choice(name="Redfish", value="redfish"),
                                app_commands.Choice(name="Green", value="green")])
    async def roulette(self, interaction: discord.Interaction, amount: int , color: app_commands.Choice[str]):
        r'''Choose a color to roll (Black, Black-Fish, Red, Red-Fish, Green). Black/Red gives 2x the amount you gave to command.
            Black-Fish/Red-Fish gives x7 the amount you gave to the command or x2 if you chose Black/Red.
            Green gives x14 the amount you gave to the command.
            
            Parameters
            -----------
            amount: class:`int` 
                The amount given by the user from balance to play roulette.
            color: class:`Choice[str]` 
                The color chosen by the user.
            
            Raises
            -----------
            mysqlconnection.Error
                User was not added to the MySQL database or something went wrong with database connection.
            ValueError
                User's balance was smaller than amount.
            '''
        await interaction.response.defer()
        author: discord.User | discord.Member = interaction.user
        author: tuple[str] = cog_helper.user_to_str(author)
        
        try:   
            data: list = get_balance(author, amount)  
            balance_amount: int = data[0]
            balance_id: int = data[1]
            
        except mysqlconnection.Error as _:
            await asyncio.sleep(1)
            await interaction.followup.send(f'Something went wrong with executing your request 😣')
            
        except ValueError as _:
            await asyncio.sleep(1)
            await interaction.followup.send(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐')      
        
        else:
            await interaction.followup.send(f'Rolling...')
            await asyncio.sleep(1)
            roll_roulette = random.choice(['black', 'black', 'blackfish', 'black', 'black', 'black', 'black', 'green', 'red', 'redfish', 'red', 'red', 'red', 'red', 'red'])
            
            if roll_roulette == color.value:
                if color.value == ('green'):
                    amount *= 14
                elif 'fish' in color.value:
                    amount *= 7
                else:
                    amount *= 2
                balance_amount += amount
                await asyncio.sleep(1)
                await interaction.followup.send(f'You won 👏👏! The color was {roll_roulette.capitalize()}')
            
            else:
                await asyncio.sleep(1)
                await interaction.followup.send(f'Unfortunately, you lost. The color was {roll_roulette.capitalize()}. Maybe try again! 🙄') 
            
            try:
                update_balance(balance_id, balance_amount)
            
            except mysqlconnection.Error as _:
                await asyncio.sleep(1)
                await interaction.followup.send(f'Something went wrong with executing your request 😣')  
            
            else:
                await asyncio.sleep(2)
                await interaction.followup.send(f'Your current balance is {balance_amount} 🧔')
        

    @app_commands.command()
    async def wordle(self, interaction: discord.Interaction, amount: int):    
            r''' Wordle, when letter is uppercase, it is somewhere in the word, when it's an emote,
                it is in a perfect place. Based on number of attempts, you get from 200%-100% times
                the amount of coins you put to the command. You have 6 chances, each chance you lose 20% of the reward.
                
                Parameters
                -----------
                amount: class:`int` 
                    The amount user gives from balance to play wordle.
                
                Raises
                -----------
                mysqlconnection.Error
                    User was not added to the MySQL database or something went wrong with database connection.
                ValueError
                    User's balance was smaller than amount.
                '''
            await interaction.response.defer()
            
            with open('wordle.json','r') as f:
                json_info = json.load(f)
            
            author: discord.User | discord.Member = interaction.user
            author: tuple[str] = cog_helper.user_to_str(author)
            
            try:   
                data: list = get_balance(author, amount)  
                balance_amount: int = data[0]
                balance_id: int = data[1]
                
            except mysqlconnection.Error as _: 
                await interaction.followup.send(f'Something went wrong with executing your request 😣')
            
            except ValueError: 
                await interaction.followup.send(f'The amount of coins you put to command is bigger than ur balance, choose another number 😐') 
            
            chances: int = 200
            
            json_words: list = json_info['$five_letter_words']
            json_letters: dict = json_info['$emotes_for_letters']
            
            random_word: str = random.choice(json_words)
            
            await interaction.followup.send(f'{random_word}')
            
            while chances != 80:

                await interaction.followup.send('Send your word 😉 😉')
                player_word = await self.bot.wait_for('message', timeout=15)
                player_word: str = str(player_word.content)
                
                while player_word not in json_words:
                    await interaction.followup.send('Your word is not in wordlist. 🤐 🤐\nSend a correct word 😜 😜')
                    player_word = await self.bot.wait_for('message', timeout=15)
                    player_word: str = player_word.content
                
                list_letters_player: list = [y for y in player_word]
                list_letters_word: list = [x for x in random_word]
                
                correct_letters: list = list_letters_player.copy()
                
                if player_word == random_word:
                    player_word_emotes = list(player_word)
                    
                    for i in range(len(player_word_emotes)):
                        player_word_emotes[i] = json_letters[player_word_emotes[i]]
                    
                    amount = amount * chances / 100
                    balance_amount += amount
                    await asyncio.sleep(1)
                    await interaction.followup.send(f'YOU HAVE WON! 😁 😁\nTHE WORD WAS: {" ".join(player_word_emotes)}\nYOUR PRIZE IS {int(amount)}! 😁 😁')
                    
                    try:
                        update_balance(balance_id, balance_amount)
                    
                    except mysqlconnection.Error as _:
                        await interaction.followup.send(f'Something went wrong with executing your request 😣')  
                    
                    finally:
                        break
                
                for i in range(len(list_letters_word)):
            
                    if list_letters_word[i] == list_letters_player[i]:
                        correct_letters[i] = json_letters[list_letters_word[i]]
                        list_letters_word[i] = '-1'
                
                for j in range(len(list_letters_word)):
                
                    if ((list_letters_player[j] in list_letters_word) and 
                        (correct_letters[j] not in json_letters.values())):
                        list_letters_word[j] = '-1'
                        correct_letters[j] = correct_letters[j].upper()
                    
                    elif (correct_letters[j] not in json_letters.values()):
                        correct_letters[j] = list_letters_player[j]  
                                
                chances -= 20
                await interaction.followup.send(f'{" ".join(correct_letters)}')
            
            if chances == 80: 
                
                try:
                    update_balance(balance_id, balance_amount)
                
                except mysqlconnection.Error as _:
                    await interaction.followup.send(f'Something went wrong with executing your request 😣')  
                
                else:
                    await asyncio.sleep(1)
                    await interaction.followup.send('Unfortunately you lost 😑\nMaybe try again! I\'m interested in taking all of your coins. 😈 😈')
          
          
def get_balance(author: str, amount: int):
    r'''Gets user's balance from database.
        
        Parameters
        -----------
        author: :class:`str`
            User's name.
        amount: :class:`int`
            Amount of coins user put to the command.
            
        Returns
        -----------
        balance_data: :class:`list`
            List containing amount of balance and balance ID.
            
        Raises
        -----------
        mysqlconnection.Error
            Something went wrong with database connection.
        ValueError
            User's balance was smaller than amount value.
        ''' 
    query: str = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id 
    FROM discord_user_balance 
    join discord_user 
    on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
    
    data: tuple = mysqlconnection.mysql_query_with_value(query, author)
    balance_amount: int = data[0]
    balance_id: int = data[1]
    if amount > balance_amount: 
        raise ValueError
    balance_amount -= amount
    balance_data = [balance_amount, balance_id]
    return balance_data
     
    
def update_balance(balance_id: int, balance_amount: int):
    r'''Updates user balance with new balance amount.
    
        Parameters
        -----------
        balance_id: :class:`int`
            ID of user's balance.
        balance_amount :class:`int`
            Amount of user's balance.
            
        Raises
        -----------
        mysqlconnection.Error
            Something went wrong with database connection.
    '''
    query: str = ("""UPDATE discord_user_balance
                SET balance_amount = %s
                WHERE balance_id = %s""")
    
    values: tuple = (balance_amount, balance_id)
    
    mysqlconnection.mysql_query_delete_update_with_value(query, values)   
        
                 
async def setup(bot):
    await bot.add_cog(GambleCog(bot))
