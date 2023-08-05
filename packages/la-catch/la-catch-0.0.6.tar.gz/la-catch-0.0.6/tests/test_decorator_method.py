import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecoratorMethod(TestCase):
    """Test if the callback is receiving the exception"""

    def setUp(self) -> None:
        self._exception = Exception("Exception")
        self._type_error = TypeError("Exception")

    def func(self, exception):
        assert exception == self._exception

    @Catch(Exception, func)
    def test_decorator(self):
        raise self._exception

    @Catch((Exception,), func)
    def test_decorator_2(self):
        raise self._exception

    def func2(self, exception):
        assert exception == self._type_error

    @Catch((Exception, TypeError), func2)
    def test_decorator_3(self):
        raise self._type_error


if __name__ == "__main__":
    unittest.main()
