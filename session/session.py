import asyncio
from contextlib import contextmanager
from time import time, sleep
import allure

STEPTIME = 0.1
TIMEOUT = 15


def waiting():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            step_time = kwargs["STEPTIME"] if kwargs.get("STEPTIME") else STEPTIME
            timeout = kwargs["TIMEOUT"] if kwargs.get("TIMEOUT") else TIMEOUT
            start = time()
            last_error = None
            while time() - start < timeout:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as error:
                    last_error = error
                    await asyncio.sleep(step_time)
            raise last_error
        return wrapper
    return decorator


def waiting_sync(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            step_time = kwargs["STEPTIME"] if kwargs.get("STEPTIME") else STEPTIME
            timeout = kwargs["TIMEOUT"] if kwargs.get("TIMEOUT") else TIMEOUT
            start = time()
            last_error = None
            while time() - start < timeout:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as error:
                    last_error = error
                    sleep(step_time)
            raise last_error

        return wrapper

    return decorator


def step(name, print_if_done, *attrs):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            _name_ = f"[{kwargs['mode']}]" + name
            with allure.step(_name_):
                try:
                    result = await func(*args, **kwargs)
                    print(print_if_done)
                    for attr in attrs:
                        _attr = (kwargs | args[0].__dict__).get(attr)
                        if _attr is not None:
                            print(_attr)
                except Exception as e:
                    if kwargs.get("driver"):
                        pass
                        # allure.attach()
                        # прикрепить скрин
                    raise e