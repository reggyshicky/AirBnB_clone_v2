#!/usr/bin/python3
"""
Renders a template that displays all
the states from the storage
"""

from flask import Flask
from models import storage
from flask import render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display all states in the storage"""
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception_object):
    """
    Flask has the capability to pass an exception object to the
    teardown functions if an exception was raised during
    request handling or if there was an error in the applicatio
    context teardown itself.If an exception occurred, you can
    inspect the exc argument to access information about the
    exception, such as its type, message, or traceback.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
