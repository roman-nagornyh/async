from threading import Thread, Event
import time


def line_creator(done: Event):
    print('Построитель линей запущен')
    while True:
        print('='*5)
        if done.wait(timeout=.1):
            break


done = Event()
ln_creator = Thread(target=line_creator, args=(done,))
ln_creator.start()
time.sleep(5)
done.set()
ln_creator.join()
print('Конец построения')
