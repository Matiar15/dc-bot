import asyncio
import os 
import discord
from discord.ext import commands

TOKEN = 'MTEwMDgxNzgzNzc3OTYwMzU0Ng.Glhc-C.y-jT_dQ7iI1i5pAEPQORAAaknJ9y3pFAzvtQlc'
ID = 973324684538052628
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e)  


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
    
    