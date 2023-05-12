import discord
from discord.ext import commands
from discord import app_commands
import mysqlconnection
import random
import asyncio
import json

class gamble_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        
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
            mysqlconnection.mysqlQueryDeleteUpdateWithValue(query, values)
            
            await asyncio.sleep(2)
            await interaction.followup.send(f'Your current balance is {balance} 🧔')
           
            
    @app_commands.command()
    @app_commands.choices(color=[app_commands.Choice(name="Black", value="black"),
                                app_commands.Choice(name="Blackfish", value="blackfish"),
                                app_commands.Choice(name="Red", value="red"),
                                app_commands.Choice(name="Redfish", value="redfish"),
                                app_commands.Choice(name="Green", value="green")])
    async def roulette(self, interaction: discord.Interaction, amount: int , color: app_commands.Choice[str]):
        '''Choose a color to roll (Black, Black-Fish, Red, Red-Fish, Green). Black/Red gives 2x the amount you gave to command.
            Black-Fish/Red-Fish gives x7 the amount you gave to the command or x2 if you chose Black/Red.
            Green gives x14 the amount you gave to the command.'''
        await interaction.response.defer()
        author = interaction.user
        author : str = str(author)
        
        values: tuple = (author,)
    
    #
    #   FIXME: change redundancy with already implemented functions
    #
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
                balance += amount
                await asyncio.sleep(1)
                await interaction.followup.send(f'You won 👏👏! The color was {roll_roulette.capitalize()}')
            else:
                await asyncio.sleep(1)
                await interaction.followup.send(f'Unfortunately, you lost. The color was {roll_roulette.capitalize()}. Maybe try again! 🙄') 
            
            query = ("""UPDATE discord_user_balance
                    SET balance_amount = %s
                    WHERE balance_id = %s""")
            values = (balance, data[0][1])
            
            mysqlconnection.mysqlQueryDeleteUpdateWithValue(query, values)
            
            await asyncio.sleep(2)
            await interaction.followup.send(f'Your current balance is {balance} 🧔')
        
    
    @app_commands.command()
    async def wordle(self, interaction: discord.Interaction, amount: int):    
            ''' Wordle, when letter is uppercase, it is somewhere in the word, when it's an emote,
                it is in a perfect place. Based on number of attempts, you get from 200%-100% times
                the amount of coins you put to the command. You have 6 chances, each chance you lose 20% of the reward.'''
            await interaction.response.defer()
            
            with open('wordle.json','r') as f:
                json_info = json.load(f)
            
            author = interaction.user
            
            try:   
                data: list = gamble_cog.__get_balance(author, amount)  
                await interaction.followup.send(f'{data}')
                balance_amount = data[0]
                balance_id = data[1]
                
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

                await interaction.followup.send('Send your word 🙂')
                player_word = await self.bot.wait_for('message', timeout=15)
                player_word: str = str(player_word.content)
                
                while player_word not in json_words:
                    await interaction.followup.send('Your word is not in wordlist.\nSend your word 🙂')
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
                    await interaction.followup.send(f'YOU HAVE WON! 😁😁\nTHE WORD WAS: {" ".join(player_word_emotes)}\nYour prize is {int(amount)}!')
                    try:
                        gamble_cog.__insert_balance(balance_id, balance_amount)
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
                    gamble_cog.__insert_balance(balance_id, balance_amount)
                except mysqlconnection.Error as _:
                    await interaction.followup.send(f'Something went wrong with executing your request 😣')  
                else:
                    await asyncio.sleep(1)
                    await interaction.followup.send('Unfortunately you lost 😑\nMaybe try again!')
          
          
    def __get_balance(author: str, amount: int):
        author : str = str(author)
        
        values: tuple = (author,)
    
        query = (""" SELECT discord_user_balance.balance_amount, discord_user_balance.balance_id 
        FROM discord_user_balance 
        join discord_user 
        on discord_user.balance_id = discord_user_balance.balance_id where discord_user.user_name = %s;""")
        
        data = mysqlconnection.mysqlQueryWithValue(query, values)
        balance : int = data[0][0]
        balance_id : int = data[0][1]
        if amount > balance: 
            raise ValueError
        balance -= amount
        
        return [balance, balance_id]
     
        
    def __insert_balance(balance_id: int, balance: int):
       
        query = ("""UPDATE discord_user_balance
                    SET balance_amount = %s
                    WHERE balance_id = %s""")
      
        values = (balance, balance_id)

        mysqlconnection.mysqlQueryDeleteUpdateWithValue(query, values)
        
    
                  
async def setup(bot):
    await bot.add_cog(gamble_cog(bot))
