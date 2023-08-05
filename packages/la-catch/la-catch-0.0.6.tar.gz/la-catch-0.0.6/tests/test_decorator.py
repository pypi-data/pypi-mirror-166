import unittest
from unittest import TestCase

from la_catch import Catch


class TestDecorator(TestCase):
    """Test if exception is being ignored"""

    def test_decorator(self):
        @Catch(Exception)
        def func():
            raise Exception()

        func()
        func()

    def test_decorator_2(self):
        @Catch((Exception,))
        def func():
            raise Exception()

        func()
        func()

    def test_decorator_3(self):
        @Catch((Exception, TypeError))
        def func():
            raise TypeError()

        func()
        func()


if __name__ == "__main__":
    unittest.main()
