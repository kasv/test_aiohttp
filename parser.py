import asyncio
from typing import List

from aiohttp import ClientSession

from settings import LIST_NEWS_URL, ITEM_NEWS_URL, NEWS_LIMIT


async def fetch(session: ClientSession, url: str) -> str:
    """  """
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()


async def fetch_all(session: ClientSession, urls: List[str]) -> List[dict]:
    """  """

    tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


async def main() -> None:
    async with ClientSession() as session:
        news_ids = await fetch(session, LIST_NEWS_URL)
        items_urls = [ITEM_NEWS_URL.format(str(news_id)) for news_id in news_ids[:NEWS_LIMIT]]

        data = await fetch_all(session, items_urls)
        print(data)
        print(len(data))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
