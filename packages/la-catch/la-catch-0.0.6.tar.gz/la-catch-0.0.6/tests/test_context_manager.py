import unittest
from unittest import TestCase

from la_catch import Catch


class TestContextManager(TestCase):
    """Test if exception is being ignored"""

    def test_context_manager(self):
        with Catch(Exception):
            raise Exception()

    def test_context_manager_2(self):
        with Catch((Exception,)):
            raise Exception()

    def test_context_manager_3(self):
        with Catch((Exception, TypeError)):
            raise TypeError()


if __name__ == "__main__":
    unittest.main()
