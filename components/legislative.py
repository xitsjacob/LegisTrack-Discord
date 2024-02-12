import asyncio
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
        congress_num = requests.get(
            f'https://api.congress.gov/v3/congress?limit=1&api_key={os.getenv("CONGRESS_API_KEY")}')
        congress_json = congress_num.json(
        ) if congress_num and congress_num.status_code == 200 else None

        unfilitered_name = congress_json['congresses'][0]['name']
        congress_name = ''.join(c for c in unfilitered_name if c.isdigit())

        return congress_name

    # Data will be contained in a matrix, and all the data matrixis will be contained in its own matrix
    async def latest_update(self):

        current_congress = await self.current_congress()

        # Placeholders
        billLimit = 10

        updated_bills = requests.get(
            f'https://api.congress.gov/v3/bill/{current_congress}?limit={billLimit}&sort=updateDate+desc&api_key={os.getenv("CONGRESS_API_KEY")}')
        bills_response = updated_bills.json()

        if 'bills' in bills_response:
            bills_data = bills_response['bills']
            if len(bills_data) > 0:
                filtered_data = []
                for bill in bills_data:
                    type = bill['type']
                    number = bill['number']
                    title = bill['title']
                    text = bill['latestAction']['text']

                    filtered_data.append(
                        [type, number, title, text],
                    )

                return filtered_data
            else:
                return None
        else:
            print('No bill key found. Potential error.')


trackers = LegislativeTracker()

# asyncio.run(trackers.latest_update())
