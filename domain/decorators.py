import time
from .exceptions import UnauthorizedAccessError
from functools import wraps
import inspect


def log_call(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            res = await func(*args, **kwargs)
            end = time.time()
            print(f"Function {func.__name__}(args={args} kwargs={kwargs}) was executed in {end - start} seconds")
            return res

        return async_wrapper

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__}(args={args} kwargs={kwargs}) was executed in {end - start} seconds")
        return res

    return sync_wrapper


def require_role(*roles):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                bound_attrs = sig.bind(*args, **kwargs)
                bound_attrs.apply_defaults()

                role = bound_attrs.arguments.get("role")

                if role not in roles:
                    raise UnauthorizedAccessError(roles)

                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_attrs = sig.bind(*args, **kwargs)
            bound_attrs.apply_defaults()

            role = bound_attrs.arguments.get("role")

            if role not in roles:
                raise UnauthorizedAccessError(roles)

            return func(*args, **kwargs)

        return sync_wrapper

    return decorator


def retry(times, exceptions):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_exception = None

                for attempt in range(times):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        print(f"Attempt {attempt + 1} for function {func.__name__}")

                raise last_exception

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} for function {func.__name__}")

            raise last_exception

        return sync_wrapper

    return decorator