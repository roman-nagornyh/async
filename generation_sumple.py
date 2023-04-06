def sub_gen():
    yield 11
    yield 22
    yield 33


def gen():
    yield 1
    for i in sub_gen():
        yield i
    yield 2


def gen_2():
    yield 1
    yield from sub_gen()
    yield 2


for i in gen_2():
    print(i)