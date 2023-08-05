import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecoratorCallbackArgs(TestCase):
    """Test if the callback is receiving the exception"""

    def setUp(self) -> None:
        self._exception = Exception("Exception")
        self._type_error = TypeError("Exception")

    def test_decorator(self):
        def test(exception):
            assert exception == self._exception

        @Catch(Exception, test)
        def func():
            raise self._exception

        func()
        func()

    def test_decorator_2(self):
        def test(exception):
            assert exception == self._exception

        @Catch((Exception,), test)
        def func():
            raise self._exception

        func()
        func()

    def test_decorator_3(self):
        def test(exception):
            assert exception == self._type_error

        @Catch((Exception, TypeError), test)
        def func():
            raise self._type_error

        func()
        func()


if __name__ == "__main__":
    unittest.main()
