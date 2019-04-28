#!/usr/bin/env python


"""
wsgi web application for calculations
supporting the following:

  * Addition
  * Subtractions
  * Multiplication
  * Division

  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def home():
    """Returns body of web page for Home page"""
    return """<h1>Welcome to the Calculator Home Page!</h1>
    <body>
        <h3>This groudbreaking calculator accepts the following operations:</h3>
        <ul>
            <li>'add' for addition</li>
            <li>'subract' for subtraction</li>
            <li>'multiply' for multiplication</li>
            <li>'divide' for division</li>
        </ul>
    </body>
    """


def no_operator(*args):
    """Returns body of web page for no operation found"""
    return """
    <body>
        <h3>Sorry, your operation was not found.</h3>
        Please try another operation
    </body>
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
    func = dispatch_d.get(f_name, no_operator)
    return func


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    chunks = path.split("/")
    func = dispatch(chunks[1])
    args = [float(x) for x in chunks[2:]]
    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
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
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
