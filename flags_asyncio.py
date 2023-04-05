import asyncio
from httpx import AsyncClient
from flags_theardpool import BASE_URL, save_flag


def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list))


async def download_one(client: AsyncClient, cc: str):
    try:
        image = await AsyncClient.get(client, f'{BASE_URL}/{cc}/{cc}.gif'.lower())
        save_flag(image.content, f'{cc}.gif')
        print(f'Флаг страны {cc} успешно сохранен')
        return cc
    except Exception as ex:
        return False


async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        to_do = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*to_do)
    return len(res)

