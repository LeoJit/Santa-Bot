import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import random   
import json
import os
import datetime
from datetime import timedelta, datetime

class Schedule(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client = client
        self.time_to_open.start()

    @tasks.loop(minutes=1)
    async def time_to_open(self):
        with open(f"{self.path}setup.json","r") as fp:
            setup_dict = json.load(fp)
            rewards_channel= setup_dict["rewards_channel"]
            time= setup_dict["time"]
            don=setup_dict["don_role"]

        c1= await self.client.fetch_channel(rewards_channel)

        with open(f"{self.path}rewards.json","r") as fp:
            rewards_uid = json.load(fp)

        await self.client.wait_until_ready()  
        timetoformat1 = time
        time1 = datetime.strptime(timetoformat1, "%H:%M")
        now = datetime.utcnow() 
        Time1 = time1.replace(year=now.year, month=now.month, day=now.day)
        time_difference_in_minutes1 = (datetime.utcnow()-Time1) / timedelta(minutes=1)

        if (time_difference_in_minutes1 >= 0.0 and time_difference_in_minutes1 < 1.0):
            await c1.send(f"<@&{don}> today's wishes have come from: \n")
            await c1.send(f"{rewards_uid}1")
            rewards_uid=""

        with open(f"{self.path}rewards.json","w") as f:
            json.dump(rewards_uid, f)


def setup(client):
    client.add_cog(Schedule(client))
        