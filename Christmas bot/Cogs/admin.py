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

class admin(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Error:** You are not allowed to use this command")
    

    @commands.command(aliases= ["Pick"])
    async def pick(self, ctx):
        with open(f"{self.path}numbers.json","r") as fp:
            numbers = json.load(fp)

        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)
            can= setup_dict["games_channel"]
            gamescan= await self.client.fetch_channel(can)

        if len(numbers)==0:
                await ctx.send("The game has ended")

        else:            
            a=0  
            while a==0:
                value=random.randint(10,99)
                if value in numbers:
                    ind= numbers.index(value)
                    msg= await ctx.send(f"The new number is: `{value}`.") 
                    await gamescan.send(f"**The new number is: `{value}`.**")
                    numbers.pop(ind)
                    a=1
                    break
                else:
                    a=0

        with open(f"{self.path}numbers.json", "w") as f:
                json.dump(numbers, f)

        with open(f"{self.path}cards.json","r") as fp:
            card_dict = json.load(fp)

        for i in range(len(card_dict)):
            card= card_dict[str(i)]
            check= str(value)
            if check in card:
                card= card.replace(check, "X")
            card_dict[str(i)]= card

        with open(f"{self.path}cards.json", "w") as f:
                json.dump(card_dict, f)

        with open(f"{self.path}players.json","r") as fp:
            uid_list = json.load(fp)

        with open(f"{self.path}cards.json","r") as fp:
            card_dict = json.load(fp)

        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)
            c1=setup_dict["rewards_channel"]
            channel=await self.client.fetch_channel(c1)

        l=list(uid_list)
        for i in range(len(l)):
            user= await self.client.fetch_user(int(l[i]))
            ucard= card_dict[str(i)]
            if ucard.count("X")==25:
                await user.send("You have won the game! Congratulations!")
                await ctx.send("**BINGO**")
                await ctx.send(f"Congratulations <@{int(l[i])}>! You have won the game!!")
                card_dict.pop(str(i))
                uid_list.pop(l[i])
            else:
                ucard_embed= discord.Embed(title= "Game on!", description= ucard, colour=discord.Colour.blurple())
                await user.send(content=None, embed= ucard_embed)

        with open(f"{self.path}cards.json", "w") as f:
                json.dump(card_dict, f)

        with open(f"{self.path}players.json", "w") as f:
                json.dump(uid_list, f)

            

        await msg.add_reaction("✅")




    @commands.command()
    async def refill(self, ctx):
        with open(f"{self.path}numbers.json","r") as fp:
            numbers = json.load(fp)

        for i in range(10,99):
            if i in numbers:
                pass
            else:
                numbers.append(i)

        await ctx.send("Refilled 👌")

        with open(f"{self.path}numbers.json", "w") as f:
            json.dump(numbers, f)

    @commands.command()
    async def end(self, ctx):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)

        uid_list={}

        with open(f"{self.path}players.json", "w") as f:
            json.dump(uid_list, f)

        file= open(f"{self.path}player_no", "r")
        a= int(file.read()) 

        b=0
        file= open(f"{self.path}player_no", "w")
        file.write(str(b))

        await ctx.send("Game ended. Thank you for playing 😃")

    @commands.command()
    async def show_players(self, ctx):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)

        p= list(uid_list)
        p_s=""


        for i in range(len(p)):
            p_s+= f"<@{int(p[i])}> "

        await ctx.send(f"There are totally {len(p)} players in the game. Best of luck!")
        await ctx.send(p_s)


def setup(client):
    client.add_cog(admin(client))
