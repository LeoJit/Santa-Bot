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

class Bingo(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Error:** You are not allowed to use this command")

    @commands.command()
    async def add_user(self, ctx, member):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)
        
        file= open(f"{self.path}player_no", "r")
        a= int(file.read()) 

        if "<@" in member:
            member= member[3:-1]
        else:
            member=member


        uid_list[member]= a
        u=await self.client.fetch_user(int(member))

        await ctx.send(f"{u} added to the game 👍")

        with open(f"{self.path}players.json", "w") as f:
            json.dump(uid_list, f)

        b=a+1
        file= open(f"{self.path}player_no", "w")
        file.write(str(b))


    @commands.command()
    async def start(self, ctx):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)

        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)
            c1=setup_dict["rewards_channel"]
            channel=await self.client.fetch_channel(c1)

        for o in range(len(uid_list)):
            list1= list(uid_list)
            user= await self.client.fetch_user(int(list1[o]))

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)

            for i in range(10,99):
                if i in numbers:
                    pass
                else:
                    numbers.append(i)

            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)

            l1=[]
            l2=[]
            l3=[]
            l4=[]
            l5=[]
            u1=""
            u2=""
            u=""
            r=""
            l=""

            for i in range(5):
                a=0  
                while a==0:
                    value=random.randint(10, 99)
                    val2=str(value)
                    if value in numbers:
                        ind= numbers.index(value)
                        if len(val2)==1:
                            val= val2 + " "
                        else:
                            val=val2
                        l1.append(val)
                        numbers.pop(ind)
                        a=1
                        break
                    else:
                        a=0

            for i in range(0, len(l1)):
                u+= str(l1[i]) +" | "
            
            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)


            for j in range(5):
                b=0  
                while b==0:
                    value=random.randint(10, 99)
                    val2=str(value)
                    if value in numbers:
                        ind= numbers.index(value)
                        if len(val2)==1:
                            val= val2 + " "
                        else:
                            val=val2
                        l2.append(val)
                        numbers.pop(ind)
                        b=1
                        break
                    else:
                        b=0


            for j in range(0, len(l2)):
                r+= str(l2[j]) +" | "


            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)


            for m in range(5):
                z=0  
                while z==0:
                    value=random.randint(10, 99)
                    val2=str(value)
                    if value in numbers:
                        ind= numbers.index(value)
                        if len(val2)==1:
                            val= val2 + " "
                        else:
                            val=val2
                        l4.append(val)
                        numbers.pop(ind)
                        z=1
                        break
                    else:
                        z=0

            for m in range(0, len(l4)):
                u1+= str(l4[m]) +" | "


            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)


            for n in range(5):
                y=0  
                while y==0:
                    value=random.randint(10, 99)
                    val2=str(value)
                    if value in numbers:
                        ind= numbers.index(value)
                        if len(val2)==1:
                            val= val2 + " "
                        else:
                            val=val2
                        l5.append(val)
                        numbers.pop(ind)
                        y=1
                        break
                    else:
                        y=0

            for n in range(0, len(l5)):
                u2+= str(l5[n]) +" | "


            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

            with open(f"{self.path}card_no.json","r") as fp:
                numbers = json.load(fp)


            for k in range(5):
                c=0  
                while c==0:
                    value=random.randint(10, 99)
                    val2=str(value)
                    if value in numbers:
                        ind= numbers.index(value)
                        if len(val2)==1:
                            val= val2 + " "
                        else:
                            val=val2
                        l3.append(val)
                        numbers.pop(ind)
                        c=1
                        break
                    else:
                        c=0

            for k in range(0, len(l2)):
                l+= str(l3[k]) +" | "

            head= f"{user}'s card"

            card= "`" + " +------------------------+ \n" + f" | {u}" + f"\n | {r}" + f"\n | {u1}" + f"\n | {u2}" +  f"\n | {l}" + "\n +------------------------+ " + "`"
            card_embed=discord.Embed(title= "Christmas Bingo Card", description= card, colour= discord.Colour.red())
            card_embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/789401994875633695/790829916954165288/bingo.jpeg")
            card_embed.set_footer(text= "All the best!!")
            card_embed1=discord.Embed(title= head, description= card, colour= discord.Colour.blue())
            await user.send(content=None, embed= card_embed)
            await channel.send(content=None, embed=card_embed1)

            with open(f"{self.path}cards.json", "r") as fp:
                card_dict= json.load(fp)

            card_dict[o]= card

            with open(f"{self.path}cards.json", "w") as f:
                json.dump(card_dict, f)


            with open(f"{self.path}card_no.json", "w") as f:
                json.dump(numbers, f)

        await ctx.send("Game started. Check your DMs for the cards. We will be picking 1 number, and if you have that number on your card, the number will turn to a `.` The first person to get an entire card of `.`s wins!")
        await ctx.send("All the best! 🎅🎄")

    @commands.command()
    async def remove_user(self, ctx, member):
        with open(f"{self.path}players.json","r") as fp:
            uid_list=json.load(fp)
        
        with open(f"{self.path}cards.json","r") as fp:
            card_dict=json.load(fp)
        

        if "<@" in member:
            member= member[3:-1]
        else:
            member=member

        u = await self.client.fetch_user(int(member))
        no= str(uid_list[member])
        card_dict.pop(no)
        uid_list.pop(str(member))

        await ctx.send(f"{u} removed to the game 👍")

        with open(f"{self.path}players.json", "w") as f:
            json.dump(uid_list, f)

        with open(f"{self.path}cards.json", "w") as f:
            json.dump(card_dict, f)


def setup(client):
    client.add_cog(Bingo(client))