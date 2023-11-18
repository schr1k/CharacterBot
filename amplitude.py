import asyncio
import json

import aiohttp

import config


async def send_event(tg: str, event: str):
    url = 'https://api2.amplitude.com/2/httpapi'
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    data = json.dumps({
        "api_key": config.AMPLITUDE_API_KEY,
        "events": [{
            "user_id": tg,
            "event_type": event
        }]
    })
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            return response.status == 200


# async def main():
#     print(await send_event('123456', 'a'))
#
#
# asyncio.run(main())
