import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import random
import json
import os
import datetime
from datetime import timedelta, datetime


class Setup(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Error:** You are not allowed to use this command")

    @commands.command()
    async def setup(self, ctx):
        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)

        a=0
        while a==0:
            await ctx.send("Please input the channel you want to set as the one where the user rewards are posted?")
            channel= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<#" in channel.content:
                channel.content = channel.content[2:-1]
            else:
                channel.content = channel.content
            
            if channel.content.isdigit():
                channel_rewards= await self.client.fetch_channel(int(channel.content))
                setup_dict["rewards_channel"]= channel_rewards.id
                a=1
                break

            else:
                await ctx.send("Try again")

        b=0
        while b==0:
            await ctx.send("Please input the games room channel.")
            channel1= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            print(channel1.content)
            if "<#" in channel1.content:
                channel1.content = channel1.content[2:-1]
            else:
                channel1.content = channel1.content
            
            if channel1.content.isdigit():
                games_channel= await self.client.fetch_channel(int(channel1.content))
                setup_dict["games_channel"]= games_channel.id
                b=1
                break

            else:
                await ctx.send("Try again")
      

        n=0
        while n==0:
            await ctx.send("Please input a role that can give rewards")
            don_role= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<@&" in don_role.content:
                don_role.content = don_role.content[3:-1]
            else:
                don_role.content = don_role.content
            
            if don_role.content.isdigit():
                setup_dict["don_role"]= int(don_role.content)
                n=1
                break

            else:
                await ctx.send("Try again")

        f=0
        while f==0:
            await ctx.send("Please input the guild id?")
            guild= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)

            if guild.content.isdigit():
                setup_dict["Guild"]= int(guild.content)
                f=1
                break

            else:
                ctx.send("Try again.")


        guild = self.client.get_guild(setup_dict["Guild"])
        don_role = discord.utils.get(guild.roles, id=setup_dict["don_role"])
        
        g=0
        while g==0:
            now = datetime.utcnow()
            time1 = datetime.strftime(now, "%H:%M:%S")
            await ctx.send(f"At what time UTC would you want to receive reminders about open suggestions? \n Current time is `{time1}`")
            time= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)

            if time.content.count(":")==1:
                setup_dict["time"]= time.content
                g=1
                break
            else:
                await ctx.send("Please try again...")
        
        with open(f"{self.path}setup.json", "w") as f:
                json.dump(setup_dict, f)

        await channel_rewards.send(f"You will be reminded daily at `{time.content}` UTC :)")
        await ctx.send("Setup complete 👌")
        await channel_rewards.send(f"Reward reminders will be sent here")   
        
    @commands.command()
    async def change_time(self, ctx):
        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)

        z=0
        while z==0:
            now = datetime.utcnow()
            time1 = datetime.strftime(now, "%H:%M:%S")
            await ctx.send(f"At what time UTC would you want to receive reminders about open suggestions? \n Current time is `{time1}`")
            time= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)

            if time.content.count(":")==1:
                setup_dict["time"]= time.content
                z=1
                break
            else:
                await ctx.send("Please try again...")

        with open(f"{self.path}setup.json", "w") as f:
                json.dump(setup_dict, f)

def setup(client):
    client.add_cog(Setup(client))



