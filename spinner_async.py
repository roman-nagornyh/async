import asyncio
import itertools
import time
from healthy_sleep import is_prime

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


async def slow() -> int:
    await asyncio.sleep(5)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin('Поехали'))
    print(f'Объект прокрутки: {spinner}')
    result = await is_prime(5_000_111_000_222_021)
    spinner.cancel()
    return result


result = asyncio.run(supervisor())
print(f'Ответ: {result}')
