import asyncio
import itertools


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


async def supervisor():
    spinner = asyncio.create_task()