import unittest
from unittest import TestCase

from la_catch import Catch


class TestContextManagerCallback(TestCase):
    """Test if the callback is receiving the exception"""

    def setUp(self) -> None:
        self._exception = Exception("Exception")
        self._type_error = TypeError("Exception")

    def test_context_manager(self):
        def test(exception):
            assert exception == self._exception

        with Catch(Exception, test):
            raise self._exception

    def test_context_manager_2(self):
        def test(exception):
            assert exception == self._exception

        with Catch((Exception,), test):
            raise self._exception

    def test_context_manager_3(self):
        def test(exception):
            assert exception == self._type_error

        with Catch((Exception, TypeError), test):
            raise self._type_error


if __name__ == "__main__":
    unittest.main()
