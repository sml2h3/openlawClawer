from __future__ import absolute_import

from app import app

@app.task
def add(x, y):
    return x + y