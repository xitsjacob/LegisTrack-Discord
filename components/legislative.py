import asyncio
import json
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv("./.env")

past_time = '2024-02-07T03:58:00Z'


class LegislativeTracker():
    def __init__(self):
        self.time_format = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

    async def current_congress(self):
        congress_num = requests.get(f'https://api.congress.gov/v3/congress?limit=1&api_key={os.getenv("CONGRESS_API_KEY")}') 
        print(congress_num.status_code)
        congress_json = congress_num.json() if congress_num and congress_num.status_code == 200 else None

        unfilitered_name = congress_json['congresses'][0]['name']
        congress_name = ''.join(c for c in unfilitered_name if c.isdigit())
        
        return congress_name

    async def latest_update(self): # Data will be contained in a matrix, and all the data matrixis will be contained in its own matrix

        current_congress = await self.current_congress()
        updated_bills = requests.get(f'https://api.congress.gov/v3/bill/{current_congress}?fromDateTime={past_time}&toDateTime={self.time_format}&sort=updateDate+desc&api_key={os.getenv("CONGRESS_API_KEY")}')

        # Data will go through a for loop, and once confirmed it actually updated. Data will be sent into a matrix. 
        # Following the completion of this for loop the data will be sent back and will begin embeding.

        print(updated_bills.json())
        return

trackers = LegislativeTracker()

asyncio.run(trackers.latest_update())
# asyncio.run(trackers.current_congress())


# updated_bills = requests.get(f'https://api.congress.gov/v3/bill?fromDateTime=2024-01-07T00%3A00%3A00Z&toDateTime=2024-02-07T00%3A00%3A00Z&sort=updateDate+desc&api_key={os.getenv("CONGRESS_API_KEY")}')
