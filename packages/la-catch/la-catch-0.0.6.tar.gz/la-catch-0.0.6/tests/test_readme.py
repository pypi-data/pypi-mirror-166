import unittest
from unittest import TestCase

from la_catch import Catch


class TestREADME(TestCase):
    """Test if exception is being ignored"""

    def test_readme(self):
        def func():
            with Catch(TypeError):
                raise TypeError("example")

        func()

        #######################################

        def on_error(exception):
            print(exception)

        def func():
            with Catch(TypeError, on_error):
                raise TypeError("example")

        func()

        #######################################

        def on_error(message, exception):
            print(message, exception)

        def func():
            with Catch(TypeError, on_error, "WARNING:"):
                raise TypeError("example")

        func()

        #######################################

        def func():
            with Catch((TypeError, FileNotFoundError)):
                raise FileNotFoundError("example")

        func()

        #######################################

        @Catch(TypeError)
        def func():
            raise TypeError("example")

        func()

        #######################################

        @Catch(TypeError, 10)
        def func():
            raise TypeError("example")

        func()

        #######################################

        def on_error(exception):
            print(exception)

        @Catch(TypeError, on_error)
        def func():
            raise TypeError("example")

        func()

        #######################################

        def on_error(message, exception):
            print(message, exception)

        @Catch(TypeError, on_error)
        def func(message="WARNING:"):
            raise TypeError("example")

        func()

        #######################################

        def on_file_not_found_error(exception):
            print(exception)

        def on_typerror(exception):
            print(exception)

        @Catch(FileNotFoundError, on_file_not_found_error)
        @Catch(TypeError, on_typerror)
        def func():
            raise TypeError("example")
            raise FileNotFoundError("example")

        func()

        #######################################


if __name__ == "__main__":
    unittest.main()
