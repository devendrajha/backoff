
from functools import wraps
import time
import logging
import random

logger = logging.getLogger(__name__)


def re_try(exceptions, total_tries=4, initial_wait=0.5, backoff_factor=2):

    def re_try_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                try:
                    print(f'{total_tries + 2 - _tries}. try:')
                    return f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    print_args = args if args else 'no args'
                    if _tries == 1:
                        msg = str(f'Function: {f.__name__}\n'
                                  f'Failed after {total_tries} tries.\n'
                                  f'args: {print_args}, kwargs: {kwargs}')
                        print(msg)
                        raise
                    msg = str(f'Function: {f.__name__}\n'
                              f'Exception: {e}\n'
                              f'Retrying in {_delay} seconds!, args: {print_args}, kwargs: {kwargs}\n')
                    print(msg)
                    time.sleep(_delay)
                    _delay *= backoff_factor

        return func_with_retries
    return re_try_decorator


if __name__ == '__main__':
    re_try(Exception, total_tries=2)