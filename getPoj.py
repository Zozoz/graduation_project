#!/usr/bin/env python
# encoding: utf-8

import re
import threading
import urllib2


class Spider(threading.Thread):
    f = 'http://poj.org/userlist?start='
    r = '&size=500&of1=solved&od1=desc&of2=submit&od2=asc'
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        i = self.id
        fp = open('poj' + str(i) + '.data', 'w')
        start = 500 * i
        url = self.f + str(start) + self.r
        while True:
            try:
                user_response = urllib2.urlopen(url).read()
                break
            except:
                print 'User-Error'
        username = re.findall('&user_id=(\w+)>', user_response)
        for j in range(len(username)):
            print start + j, ':', username[j]
            fp.write(username[j])
            url = 'http://poj.org/userstatus?user_id=' + username[j]
            while True:
                try:
                    problem_response = urllib2.urlopen(url).read()
                    break
                except:
                    print 'Problem-Error'
            problem = re.findall('p\((\w+)\)', problem_response)
            for i in range(1, len(problem)):
                fp.write(' ' + problem[i])
            fp.write('\n')


def crawl():
    threads = []
    for i in range(10, 20):
        while True:
            try:
                threads.append(Spider(i))
                break
            except:
                print 'Thread-Error'

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def joinFile():
    fp = open('poj.data', 'a+')
    cnt = 0
    for i in range(10, 20):
        with open('poj' + str(i) + '.data', 'r') as f:
            for line in f:
                cnt += 1
                print  cnt
                fp.write(line)


if __name__ == '__main__':
    # crawl()
    joinFile()


