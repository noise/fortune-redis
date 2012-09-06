#!/usr/bin/python
'''
Simple HTTP API for random fortunes
'''
from flask import Flask
from flask import request
from fortuneRedis import FortuneRedis

app = Flask(__name__)

@app.route('/')
def randomFortune():
    id = request.args['id'] or request.remote_addr
    print 'id = %s' % id
    return fr.randomFortune()

@app.route('/mod/<module>')
def randomFortuneMod(module):
    return fr.randomFortune(module)
    

if __name__ == '__main__':
    app.debug = True
    fr = FortuneRedis()
    app.run()
    
