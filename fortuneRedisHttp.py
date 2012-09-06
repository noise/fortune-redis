#!/usr/bin/python
'''
Simple HTTP API for random fortunes
'''
from flask import Flask
from fortuneRedis import FortuneRedis

app = Flask(__name__)

@app.route('/')
def randomFortune():
    return fr.randomFortune()

@app.route('/mod/<module>')
def randomFortuneMod(module):
    return fr.randomFortune(module)
    

if __name__ == '__main__':
    app.debug = True
    fr = FortuneRedis()
    app.run()
    
