import asyncio
import json

import aiohttp


async def make_request(system_message: str, user_message: str):
    url = 'http://95.217.14.178:8080/candidates_openai/gpt'
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    })
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            return await response.json()


# async def main():
#     print(await make_request('a', 'b'))
#
#
# asyncio.run(main())
