import asyncio
import discord
import requests
import os
from components.legislative import LegislativeTracker
from discord.ext import commands
from dotenv import load_dotenv

NEWS_TRACKER = False
EXECUTIVE_TRACKER = False
LEGISLATIVE_TRACKER = True
JUDICIAL_TRACKER = False

load_dotenv("./.env")

class Trackers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Trackers are ready')
    
    @commands.command()
    async def leg(self, ctx):
        try:
            tracker = LegislativeTracker()
            await tracker.latest_update()
            await ctx.send('done')
        except:
            await ctx.send("Error...")

async def setup(client):
    await client.add_cog(Trackers(client))