import asyncio
import uuid

import httpx

sem = asyncio.Semaphore(20)


async def send_request(url: str, client: httpx.AsyncClient, i: int):
    async with sem:
        print(f"send {i}")
        await client.post(url, params={"link": str(uuid.uuid4())})
        print(f"recieved {i}")


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [
            send_request("http://localhost:8000/link", client, i) for i in range(10000)
        ]
        await asyncio.gather(*tasks)


asyncio.run(main())
