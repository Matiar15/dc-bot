import discord
from discord.ext import commands
from discord import app_commands
import asyncpraw
import json
import random


with open("token.json", 'r') as raw_data:
    data = json.load(raw_data)

data = data['$praw'] # Getting reddit bot's data from .json file

reddit = asyncpraw.Reddit(client_id = data['client_id']
                     ,client_secret = data['client_secret']
                     ,username = data['username']                   
                     ,password = data['password']
                     ,user_agent = data['user_agent'])
reddit.read_only = True


class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description="Display a meme! 😆")
    async def meme(self, interacion: discord.Interaction):
        r'''Gets a random meme from reddit's subreddit.
        '''
        sub_reddit: reddit.SubredditHelper = await reddit.subreddit("memes")
        sub_reddit = sub_reddit.top(limit=50, time_filter="week")
        all_posts: list = []
        async for i in sub_reddit:
            all_posts.append(i)

        random_post = random.choice(all_posts)
        post_name = random_post.title
        post_url = random_post.url
        post_embed = discord.Embed(title = post_name)
        post_embed.set_image(url = post_url)
        await interacion.response.send_message(embed=post_embed)


async def setup(bot):
    await bot.add_cog(RedditCog(bot))
    