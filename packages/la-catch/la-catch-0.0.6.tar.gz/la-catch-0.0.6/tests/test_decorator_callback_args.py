import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecoratorCallbackArgs(TestCase):
    """
    Test if arguments from function and exception
    are being pass to callback
    """

    def setUp(self) -> None:
        self._exception = Exception("Exception")

    def test_decorator(self):
        def test(a, b, exception):
            assert a == 1
            assert b == 2
            assert exception == self._exception

        @Catch(Exception, test)
        def func(a, b):
            raise self._exception

        func(1, 2)
        func(1, 2)

    def test_decorator_2(self):
        def test(a, b, exception):
            assert a == 1
            assert b == 2
            assert exception == self._exception

        @Catch(Exception, test)
        def func(a, b):
            raise self._exception

        func(1, b=2)
        func(1, b=2)

    def test_decorator_3(self):
        def test(a, b, exception):
            assert a == 1
            assert b == 2
            assert exception == self._exception

        @Catch(Exception, test)
        def func(a, b):
            raise self._exception

        func(a=1, b=2)
        func(a=1, b=2)


if __name__ == "__main__":
    unittest.main()
