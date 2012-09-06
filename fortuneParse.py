#!/usr/bin/python

'''
Parse the given fortune file and return contained fortunes as a list
'''
def parse(path):
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
        return fortunes
    except Exception, e:
        print 'Exception ', e
    finally:
        if f:
            f.close()


if __name__ == '__main__':
    #error test
    fortuneModParse('fortunes/sdfdsfd')
    # positive test
    fortunes = fortuneModParse('fortunes/bofh-excuses')
    #print fortunes
