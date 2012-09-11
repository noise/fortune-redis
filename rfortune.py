#!/usr/bin/python

from optparse import OptionParser

import os
import redis


class Fortune(object):
    '''
    Model for a fortune.
    '''

    SLEN = 160  # max chars for a 'short' fortune
    PATH_FMT = 'fortunes/%(id)s/%(mod)s'

    def __init__(self, id, mod, text):
        self.id = id
        self.mod = mod
        self.text = text

    def path(self):
        return self.PATH_FMT % self.__dict__

    def is_short(self):
        return len(self.text) <= self.SLEN

    def as_html(self):
        return '<div id="%s"><pre>%s</pre></div>' \
               % (self.path(), self.text)

    def __repr__(self):
        return 'id: %s, mod: %s,\n%s' % (self.id, self.mod, self.text)


class Fortunes(object):
    '''
    Handles loading fortune-mod data into Redis and and retrieving them
    at random. A set of fortunes is referred to as a 'module' to avoid
    confusion with the Redis sets used for storage.
    '''
    FID_KEY = 'fid'  # key for id counter
    MODS_KEY = 'fmods'  # key for set of module names

    def __init__(self, host=None):
        '''
        Host for redis connection, defaults to 'localhost'.
        '''
        self.host = host or 'localhost'
        self.r = redis.Redis(self.host)

    def parse(self, path):
        '''
        Parses the given fortune data file and return contained fortunes as
        a list of strings.
        Fortune files are expected to contain fortunes separated by a
        single '%' character on its own line.
        '''
        fortunes = []
        f = None
        try:
            f = open(path)
            entry = ""
            for l in f:
                if ('%' not in l):
                    entry += l
                else:
                    fortunes.append(entry)
                    entry = ""
            fortunes.append(entry)  # final entry
            return fortunes
        finally:
            if f:
                f.close()

    def mod_key(self, mod):
        return 'fmod/%s' % mod

    def fortune_key(self, fid):
        return 'f/%s' % fid

    def load_to_redis(self, path, mod):
        '''
        Reads the given fortune data file and and loads into a Redis set.
        :param path: filesystem path of fortune-mod data file
        :param mod: name of the module(set) of fortunes
        '''
        try:
            fortunes = self.parse(path)
        except Exception, e:
            print 'Exception parsing %s' % path, e
            raise

        # clean out old fortunes and mod set if exists
        modkey = self.mod_key(mod)
        if (self.r.exists(modkey)):
            for fid in self.r.smembers(modkey):
                self.r.delete(self.fortune_key(fid))
            self.r.delete(modkey)

        # add new
        for f in fortunes:
            fid = self.r.incr(self.FID_KEY)
            self.r.set(self.fortune_key(fid), f)
            self.r.sadd(modkey, fid)
        self.r.sadd(self.MODS_KEY, mod)
        print 'loaded %d fortunes from %s' % (self.r.scard(modkey), path)

    def random_fortune_id(self, mod):
        '''
        Select a random fortune ID from the given module and return it.
        :param mod: name of fortune module to select from
        '''
        return self.r.srandmember(self.mod_key(mod))

    def random_fortune(self, mod=None):
        '''
        Select a random Fortune from the given module and return it.
        :param mod: name of fortune module, chosen randomly if omitted
        '''
        if (mod is None):
            mod = self.r.srandmember(self.MODS_KEY)
        fid = self.random_fortune_id(mod)
        text = self.r.get(self.fortune_key(fid))
        return Fortune(fid, mod, text)


if __name__ == '__main__':
    ''' cmdline usage for performing the initial data load to redis '''
    usage = "usage: %prog [option] pattern"
    parser = OptionParser(usage=usage)
    parser.add_option("--host", dest="host", default="localhost",
                      help="redis host")
    parser.add_option("--path", dest="path", default="fortunes",
                      help="path to directory of fortune-mod files")
    (options, args) = parser.parse_args()

    fr = Fortunes(options.host)

    for filename in os.listdir(options.path):
        if not ('.u8' in filename or '.dat' in filename or '.md' in filename):
            fr.load_to_redis(options.path + '/' + filename, filename)

    #print 'testing...'
    #print fr.random_fortune()
    #print fr.random_fortune('foo')
    #print fr.random_fortune('bofh-excuses')
