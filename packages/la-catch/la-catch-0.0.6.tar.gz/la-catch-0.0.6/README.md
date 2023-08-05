# la-catch
Decorator and context manager to catch exception(s) and call a function to handle the error.  

# install
`pip install la-catch`  

# usage
There is two ways to use `catch`:
- Context Manager
- Decorator

# context manager
Catch exception and do nothing:  

```python
from la_catch import Catch

def func():
    with Catch(TypeError):
        raise TypeError("example")
```

Catch exception and call callback passing exception:  

```python
from la_catch import Catch

def on_error(exception):
    print(exception)

def func():
    with Catch(TypeError, on_error):
        raise TypeError("example")
```

Catch exception and call callback passing keywords arguments and exception:  

```python
from la_catch import Catch

def on_error(message, exception):
    print(message, exception)

def func():
    with Catch(TypeError, on_error, "WARNING:"):
        raise TypeError("example")
```

Catch multiple exceptions:  

```python
from la_catch import Catch

def func():
    with Catch((TypeError, FileNotFoundError)):
        raise FileNotFoundError("example")
```


# decorator
Make sure that the callback signature identical to the function signature.  
Catch exception and return `None`:  

```python
from la_catch import Catch

@Catch(TypeError)
def func():
    raise TypeError("example")
```

Catch exception and return a value:   

```python
from la_catch import Catch

@Catch(TypeError, 10)
def func():
    raise TypeError("example")
```

Catch exception and call callback passing exception:   

```python
from la_catch import Catch

def on_error(exception):
    print(exception)

@Catch(TypeError, on_error)
def func():
    raise TypeError("example")
```

Catch exception and call callback passing decorated function arguments and exception:   

```python
from la_catch import Catch

def on_error(message, exception):
    print(message, exception)

@Catch(TypeError, on_error)
def func(message="WARNING:"):
    raise TypeError("example")
```

Chain catchs:  

```python
from la_catch import Catch

def on_file_not_found_error(exception):
    print(exception)

def on_typerror(exception):
    print(exception)

@Catch(FileNotFoundError, on_file_not_found_error)
@Catch(TypeError, on_typerror)
def func():
    raise FileNotFoundError("example")
    raise TypeError("example")
```

# notes
Initialization arguments are used by context manager and ignored by decorators, because:  
- Would have to decide a priority between intialization arguments and function arguments  
- Passing default values to callback would need me to know the function arguments  
    - When chaining decorators, wasn't possible to discover the function parameters because decorators would give `(*args, **kwargs)`  
    - When chaining decorators, wasn't possible to discover the default values because decorators would give `(*args, **kwargs)`  
