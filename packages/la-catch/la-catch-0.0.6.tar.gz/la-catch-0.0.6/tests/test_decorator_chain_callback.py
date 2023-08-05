import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecoratorChainCallback(TestCase):
    """Test if is possible to chain Catchs"""

    def setUp(self) -> None:
        self._type_error = TypeError()
        self._file_not_found = FileNotFoundError()

    def test_decorator(self):
        def on_file_error(exception):
            assert exception == self._file_not_found

        def on_type_error(exception):
            assert exception == self._type_error

        @Catch(FileNotFoundError, callback=on_file_error)
        @Catch(TypeError, callback=on_type_error)
        def func():
            raise self._type_error

        func()
        func()

    def test_decorator_2(self):
        def on_file_error(exception):
            assert exception == self._file_not_found

        def on_type_error(exception):
            assert exception == self._type_error

        @Catch(FileNotFoundError, callback=on_file_error)
        @Catch(TypeError, callback=on_type_error)
        def func():
            raise self._file_not_found

        func()
        func()


if __name__ == "__main__":
    unittest.main()
