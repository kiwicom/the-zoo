import random


def check_randomly(context):
    yield context.Result("constant:sometimes_found", random.choice([True, False]))

    yield context.Result("constant:rarely_found", random.choice([False] * 9 + [True]))
    yield context.Result("constant:often_found", random.choice([True] * 9 + [False]))
