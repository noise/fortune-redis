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
def random_fortune():
    id = user_id(request)
    return f.random_fortune(None, id).as_html()


@app.route('/mod/<module>')
def random_fortune_mod(module):
    id = user_id(request)
    return f.random_fortune(module, id).as_html()


@app.route('/modules')
def modules():
    return ', '.join(f.module_list())


@app.route('/users/me')
def user_stats_me():
    return f.user_stats(user_id(request))


@app.route('/help')
def help():
    return '''
<pre>
/: random fortune from all sets
/mod/<module>: random fortune from a given set
/modules/: list of modules
/users/me: user stats
</pre>
'''

if __name__ == '__main__':
    app.debug = True
    f = Fortunes()
    app.run(host='0.0.0.0')
