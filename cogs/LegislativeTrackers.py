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


class LegislativeTrackers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Trackers are ready')

    @commands.command()
    async def leg(self, ctx):
        try:
            tracker = LegislativeTracker()
            recent_bills = await tracker.latest_update()

            # type [0], number [1], title [2], text [3]

            embedTitle = "Legislative Bill's Updates"
            embedDesc = "NOTE: Long bill names will be cut off to prevent errors. In order to recieve the full title you will need to do the following command: !bill type number"
            legislativeUpdate = discord.Embed(title=embedTitle, description=embedDesc)
            legislativeUpdate.set_thumbnail(url='https://media.discordapp.net/attachments/1204202118408568873/1204202612417765406/legistrack_logo.png?ex=65d3e013&is=65c16b13&hm=11eb780032939d7655a9f0b4cb85987ad2476a6d1abd7d28dc136200de9a5113&=&format=webp&quality=lossless&width=905&height=905')
            
            for bill in recent_bills:
                type = bill[0]
                number = bill[1]
                title = bill[2][:200]
                text = bill[3]

                legislativeUpdate.add_field(name=f"{type}. {number} | {title}", value=f"{text}", inline=False)

            legislativeUpdate.set_footer(text="For more info on a bill do: !bill type number")
            
            await ctx.send(embed=legislativeUpdate)
        except Exception as e:
            dev_id = int(os.getenv("DEV_USER_ID"))
            await ctx.send(f"<@{dev_id}> Error: {e}")


async def setup(client):
    await client.add_cog(LegislativeTracker(client))
