#  Write a simple timeout decorator
from time import sleep
import signal

def raise_timeout(*args, **kwargs):
    raise TimeoutError

def timer(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signalnum=signal.SIGALRM, handler=raise_timeout)
            signal.alarm(seconds)
            func(*args, **kwargs)
            signal.alarm(0)
        return wrapper
    return decorator

@timer(20)
def foo():
    print("Starting foo")
    sleep(5)
    print("Ending foo")

try:
    foo()
    print("foo() completed")
except TimeoutError:
    print("foo() timed out")