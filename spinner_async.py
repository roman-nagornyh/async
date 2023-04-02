import asyncio
import itertools
import time
from healthy_sleep import is_prime
import aiohttp


async def spin(msg: str):
    for char in itertools.cycle(r'\|/'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' '*len(status)
    print(f'\r{blanks}\r', end='')


async def get_actual_marks():
    url = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'token': ''}) as res:
            print(res.status)
            return await res.text()


async def supervisor():
    spinner = asyncio.create_task(spin('Получение информации с api'))
    print(f'Объект прокрутки: {spinner}')
    result = await get_actual_marks()
    spinner.cancel()
    return result


result = asyncio.run(supervisor())
print(f'Ответ: {result}')
