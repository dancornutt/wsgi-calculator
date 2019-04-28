#!/usr/bin/env python

import pprint

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def home():
    """Returns body of web page for Home page"""
    return """Welcome to the home page!
    this groudbreaking calculator accepts the following operations:
        'add' for addition
        'subract' for subtraction
        'multiply' for multiplication
        'divide' for division


    """


def divide(*args):
    """ Returns a STRING with the division of the arguments """
    total = args[0]
    for value in args[1:]:
        total /= value
    return str(total)


def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """
    total = args[0]
    for value in args[1:]:
        total *= value
    return str(total)


def subtract(*args):
    """ Returns a STRING with the subraction of the arguments """
    total = args[0]
    for value in args[1:]:
        total -= value
    return str(total)


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for value in args:
        sum += value
    return str(sum)


def dispatch(f_name):
    """Dispatch dictionary for pages of web app"""
    dispatch_d = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
        "": home,
    }
    func = dispatch_d.get(f_name)
    return func


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    # args = ['25', '32']
    chunks = path.split("/")
    print("function chunk is: {}".format(chunks[1]))
    func = dispatch(chunks[1])
    args = [float(x) for x in chunks[2:]]
    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    # pprint.pprint(environ)
    print("In App func")
    headers = [('Content-type', 'text/html')]
    try:
        print("In try loop")
        path = environ.get('PATH_INFO', None)
        if path is None:
            print("path is None! path={}".format(path))
            raise NameError
        print("Path ISNT None")
        func, args = resolve_path(path)
        body = func(*args)
        print("body= {}".format(body))
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
