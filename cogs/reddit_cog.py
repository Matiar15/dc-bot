import discord
from discord.ext import commands
from discord import app_commands
import asyncpraw
import json
import random

with open("token.json", 'r') as raw_data:
    data = json.load(raw_data)

data = data['$praw']

reddit = asyncpraw.Reddit(client_id = data['client_id']
                     ,client_secret = data['client_secret']
                     ,username = data['username']
                     ,password = data['password']
                     ,user_agent = data['user_agent'])
reddit.read_only = True


class reddit_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description="Display a meme! 😆")
    async def meme(self, interacion: discord.Interaction):
        sub_red = await reddit.subreddit("memes")
        sub_red = sub_red.top(limit=50, time_filter="week")
        sub_list = []
        async for i in sub_red:
            sub_list.append(i)

        ran_sub = random.choice(sub_list)
        name = ran_sub.title
        url = ran_sub.url
        embed = discord.Embed(title = name)
        embed.set_image(url = url)
        await interacion.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(reddit_cog(bot))