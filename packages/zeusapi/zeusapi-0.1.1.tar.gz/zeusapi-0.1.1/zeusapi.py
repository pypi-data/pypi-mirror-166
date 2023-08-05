"""zeusapi.py
--
Core utilites for https://app.zeusapi.io, a service that allows users to
rapidly create microservices from legacy Python code.
"""
__version__ = "0.1.1"
__description__ = """Core utilites for https://app.zeusapi.io, a service that
allows users to rapidly create microservices from legacy Python code."""
import functools
from io import StringIO
import json
import pandas as pd


def zeus_data(
    _func=None,
    *,
    name=None,
    file_type=None,
    in_library=True,
    local=True,
    zeus_payload={}
):
    """Define a function to be a data source. If local, we will load the data
    locally, as defined in the function; otherwise we will expect it to be
    passed in via the POST request."""

    def decorator_zeus_data(func):
        @functools.wraps(func)
        def wrapper_zeus_data(*args, **kwargs):
            if local:
                # Let the usual function handle it.
                value = func(*args, **kwargs)
            else:
                # We will process the incoming, posted file.
                if file_type.lower() == "csv":
                    # Create a pandas dataframe.
                    datafile = zeus_payload[name].decode()
                    datafile_io = StringIO(datafile)
                    csv_dataframe = pd.read_csv(datafile_io)
                    value = csv_dataframe
                elif file_type.lower() == "json":
                    # Decode the data and return as a dictionary.
                    value = zeus_payload[name]
            return value

        return wrapper_zeus_data

    if _func is None:
        return decorator_zeus_data
    else:
        return decorator_zeus_data(_func)


def zeus_endpoint(_func=None, *, name=None):
    """Define a function to be a data source. If local, we will load the data
    locally; otherwise we will expect it to be passed in via the POST
    request."""

    def decorator_zeus_endpoint(func):
        @functools.wraps(func)
        def wrapper_zeus_endpoint(*args, **kwargs):
            value = func(*args, **kwargs)
            # value["age"] = 45
            return value

        return wrapper_zeus_endpoint

    if _func is None:
        return decorator_zeus_endpoint
    else:
        return decorator_zeus_endpoint(_func)
