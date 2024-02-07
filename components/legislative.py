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


    async def latest_update(self):
        
        updated_bills = requests.get(f'https://api.congress.gov/v3/bill?fromDateTime={past_time}&toDateTime={self.time_format}&sort=updateDate+desc&api_key={os.getenv("CONGRESS_API_KEY")}')

        print(updated_bills.json())
        return self.time_format

trackers = LegislativeTracker()

asyncio.run(trackers.latest_update())


# updated_bills = requests.get(f'https://api.congress.gov/v3/bill?fromDateTime=2024-01-07T00%3A00%3A00Z&toDateTime=2024-02-07T00%3A00%3A00Z&sort=updateDate+desc&api_key={os.getenv("CONGRESS_API_KEY")}')
