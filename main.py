import itertools
import time
from threading import Thread, Event
# Текущая страница книги 654


def spin(msg: str, done: Event):
    for char in itertools.cycle(r'\|/'):
        status = f'{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
        blanks = ' '*len(status)
        print(f'\r{blanks}\r', end='')


def slow() -> int:
    time.sleep(3)
    return 42


def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=('Ожидайте', done))
    print(f'объект прокрутки:{spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


result = supervisor()
print('')
print('')
print(f'Ответ : {result}')
