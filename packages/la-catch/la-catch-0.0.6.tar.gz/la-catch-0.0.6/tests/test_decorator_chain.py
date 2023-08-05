import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecoratorChain(TestCase):
    """Test if is possible to chain Catchs"""

    def test_decorator(self):
        @Catch(FileNotFoundError)
        @Catch(TypeError)
        def func():
            raise TypeError()

        func()
        func()

    def test_decorator_2(self):
        @Catch(FileNotFoundError)
        @Catch(TypeError)
        def func():
            raise FileNotFoundError()

        func()
        func()


if __name__ == "__main__":
    unittest.main()
