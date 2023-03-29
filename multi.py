import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.07):
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


def supervisor() -> None:
    done = Event()
    spinner = Process(target=spin, args=('Работа процесса', done))
    print(f'Объект прокрутки {spinner}')
    spinner.start()
    time.sleep(5)
    done.set()
    spinner.join()


supervisor()