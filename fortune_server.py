#!/usr/bin/python
'''
Simple HTTP API for random fortunes
'''
from flask import Flask
from flask import request
from rfortune import Fortunes

app = Flask(__name__)


def user_id(request):
    if request.args and request.args['id']:
        return request.args['id']
    else:
        return request.remote_addr


@app.route('/')
def randomFortune():
    id = user_id(request)
    return f.random_fortune().as_html()


@app.route('/mod/<module>')
def randomFortuneMod(module):
    return f.random_fortune(module).as_html()


if __name__ == '__main__':
    app.debug = True
    f = Fortunes()
    app.run()
