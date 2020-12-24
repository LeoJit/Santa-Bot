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

class UserCommands(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    @commands.command()
    async def wish(self, ctx, member):
        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)
            staff= await self.client.fetch_channel(setup_dict["rewards_channel"])
        await ctx.message.delete()
        if "<@" in member:
            member= member[3:-1]
        else:
            member=member

        user_id= await self.client.fetch_user(member)

        await ctx.author.send("Please enter the wished you would like to send to your friend :)")
        wish= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel,  discord.channel.DMChannel), timeout=300)

        message= wish.content
        user2= await self.client.fetch_user(ctx.author.id)
        title1= f"Wishes from {user2}"
        embed1= discord.Embed(title= title1, description= message, colour= discord.Colour.green())
        embed1.set_thumbnail(url= "https://cdn.discordapp.com/attachments/789401994875633695/789410185433186314/thumbnail.jpg")
        embed1.set_footer(text= "🎅🎄 Merry Christmas and a Happy New Year! 🎄🎅")

        await ctx.author.send("Are you sure you want to send these wishes?")
        final_wish= await ctx.author.send(content=None, embed=embed1)

        await final_wish.add_reaction("✅")
        await final_wish.add_reaction("❌")
        em_list1=['✅', '❌']
        def r_check(reaction: Reaction, user: Member):
            return reaction.message.id == final_wish.id and user == ctx.author and str(reaction.emoji) in em_list1

        try:
            reaction, _ = await ctx.bot.wait_for('reaction_add', check=r_check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.author.send("Sorry, you timed out.")

        if reaction.emoji=="✅":
            await ctx.author.send("Wishes sent!")
            await staff.send(f"New wish to {user_id}")
            await staff.send(content=None, embed=embed1)
            await user_id.send(f"You have a new wish from {user2}")
            await user_id.send(content=None, embed=embed1)
            rewards+= str(ctx.author.id) + " "

        if reaction.emoji== '❌':
            await ctx.author.send("Cancelled")
            return


    @commands.command(description= "Joins the game", brief= "Joins the game")
    async def join(self,ctx):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)
        
        file= open(f"{self.path}player_no", "r")
        a= int(file.read()) 

        member= ctx.author.id
        
        if str(member) in uid_list:
            await ctx.send("You have already joined the game. Please wait for it to start.")
        else:
            uid_list[member]= a
            u=await self.client.fetch_user(int(member))
            await ctx.send(f"{u} added to the game 👍")

        with open(f"{self.path}players.json", "w") as f:
            json.dump(uid_list, f)

        b=a+1
        file= open(f"{self.path}player_no", "w")
        file.write(str(b))


def setup(client):
    client.add_cog(UserCommands(client))
