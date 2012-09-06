#!/usr/bin/python

from optparse import OptionParser

import os
import redis
import fortuneParse

'''
FortuneRedis handles loading fortune-mod data into Redis
and and retrieving them at random
'''
class FortuneRedis:
    slen = 160 # max chars for a 'short' fortune
    
    def __init__(self, host=None):
        self.host = host or 'localhost'
        self.r = redis.Redis(self.host)

    '''
    path - filesystem path of fortune-mod data file
    mod - name of the module
    '''
    def loadToRedis(self, path, mod):
        # todo: check for errs
        fortunes = fortuneParse.parse(path)

        # clean out old fortunes and mod set
        modkey = 'fmod/' + mod
        if (self.r.exists(modkey)):
            for fid in self.r.smembers(modkey):
                self.r.delete('f/' + str(fid))
            self.r.delete(modkey)
    
        for f in fortunes:
            fid = self.r.incr('fid')
            self.r.set('f/' + str(fid), f)
            self.r.sadd(modkey, fid)
        self.r.sadd('fmods', mod)
        print 'loaded %d fortunes from %s' % (self.r.scard(modkey), path)

    '''
    mod - name of fortune set
    '''
    def randomFortuneId(self, mod):
        return self.r.srandmember('fmod/' + mod)

    '''
    mod - name of fortune set, if omitted choose randomly
    '''
    def randomFortune(self, mod=None):
        if (mod is None):
            mod = self.r.srandmember('fmods')
        fid = self.randomFortuneId(mod)
        return self.r.get('f/' + str(fid))

'''
Main
'''
if __name__ == '__main__':
    usage = "usage: %prog [option] pattern"
    parser = OptionParser(usage=usage)
    parser.add_option("--host", dest="host", default="localhost", help="redis host")
    parser.add_option("--path", dest="path", default="fortunes", help="path to directory of fortune-mod files")
    (options, args) = parser.parse_args()

    fr = FortuneRedis(options.host)

    for filename in os.listdir(options.path):
        if not ('.u8' in filename or '.dat' in filename):
            fr.loadToRedis(options.path + '/' + filename, filename)

    #print 'testing...'
    #print fr.randomFortune()
    #print fr.randomFortune('foo')
    #print fr.randomFortune('bofh-excuses')
