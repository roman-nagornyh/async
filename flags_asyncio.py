import asyncio
import time
from typing import Callable

from httpx import AsyncClient
from flags_theardpool import BASE_URL, save_flag, DEST_DIR, POP20_CC


def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list))


async def download_one(client: AsyncClient, cc: str):
    image = await client.get(f'{BASE_URL}/{cc}/{cc}.gif'.lower())
    save_flag(image.content, f'{cc}.gif')
    print(f'Флаг страны {cc} успешно сохранен')
    return cc


async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        to_do = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*to_do)
    return len(res)


def main(downloader: Callable[[list[str]], int]):
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n {count} загружено за {elapsed:2f}s')


main(download_many)
