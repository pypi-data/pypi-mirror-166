from asyncio import iscoroutinefunction
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

from la_catch.utility import get_arguments

P = ParamSpec("P")
R = TypeVar("R")


class Catch:
    def __init__(
        self,
        exceptions: Exception | tuple[Exception] = Exception,
        callback: Callable | Awaitable | Any = None,
        *args,
        **kwargs,
    ):
        if not isinstance(exceptions, tuple):
            exceptions = (exceptions,)

        self._exceptions = exceptions
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

        self.callback_return = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> bool:
        if type not in self._exceptions:
            return False

        self._kwargs |= {"exception": value}

        if callable(self._callback):
            self.callback_return = self._callback(*self._args, **self._kwargs)
        else:
            self.callback_return = self._callback

        return True

    def __call__(self, func: Callable[P, R]) -> Callable[P, R | Any]:
        def wrapper(*args, **kwargs):
            args, kwargs = get_arguments(func=func, args=args, kwargs=kwargs)

            with self.__class__(
                self._exceptions,
                self._callback,
                *args,
                **kwargs,
            ) as catch:
                return func(*args, **kwargs)
            return catch.callback_return  # when context manager above raise exception

        async def awrapper(*args, **kwargs):
            args, kwargs = get_arguments(func=func, args=args, kwargs=kwargs)

            async with self.__class__(
                self._exceptions,
                self._callback,
                *args,
                **kwargs,
            ) as catch:
                return await func(*args, **kwargs)
            return catch.callback_return  # when context manager above raise exception

        if iscoroutinefunction(func):
            return awrapper
        return wrapper

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback) -> bool:
        if type not in self._exceptions:
            return False

        self._kwargs |= {"exception": value}

        if callable(self._callback) and iscoroutinefunction(self._callback):
            self.callback_return = await self._callback(*self._args, **self._kwargs)
        elif callable(self._callback):
            self.callback_return = self._callback(*self._args, **self._kwargs)

        return True
