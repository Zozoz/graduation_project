#!/usr/bin/env python
# encoding: utf-8


def process_rules(filename):
    fp = open('rules.data', 'w')
    with open(filename, 'r') as f:
        for line in f:
            line = line.lstrip('(').rstrip(')\n').split(']), ')
            line[0] = line[0].lstrip('frozenset([')
            line[1] = line[1].lstrip('frozenset([]')
            fp.write(line[0] + ';' + line[1] + ';' +line[2] + '\n')
    fp.close()
    rules = []
    with open('rules.data', 'r') as f:
        for line in f:
            line = line.split(';')
            line[0] = line[0].split(', ')
            line[0] = frozenset([x.strip("'") for x in line[0]])
            line[1] = line[1].split(', ')
            line[1] = frozenset([x.strip("'") for x in line[1]])
            line[2] = float(line[2].strip('\n'))
            rules.append((line[0], line[1], line[2]))
    rules.sort(key=lambda x: x[2])
    print '-' * 15, 'rules', '-' * 15
    for item in rules:
        print item
    return rules


def process_user(filename):
    userdata = {}
    with open(filename, 'r') as f:
        cnt = 0
        for line in f:
            line = line.split(' ')
            line[-1] = line[-1].strip('\n')
            userdata[line[0]] = frozenset(line[1:])
            cnt += 1
            if cnt == 3887:
                break
    print '-' * 15, 'userdata', '-' * 15
    for k in userdata:
        print k, ' : ', userdata[k]
    return userdata


from itertools import chain, combinations
def subsets(arr):
    return chain(*[combinations(arr, i+1) for i, a in enumerate(arr) if i < 2])

def get_recommend(userdata, rules):
    commom = set(['1000', '1004', '1003', '1005', '1007', '1006', '1163', '1088', '1002', '1050'])
    ret = {}
    for k in userdata:
        tmp = set()
        data = map(frozenset, [x for x in subsets(userdata[k])])
        for item in data:
            for rule in rules:
                if item.issubset(rule[0]):
                    tmp.add(rule[1])
        for item in tmp:
            for it in item:
                if ret.has_key(k):
                    ret[k].add(it)
                else:
                    ret[k] = set([it])
        add = commom - userdata[k]
        if ret.has_key(k):
            ret[k] = ret[k] | commom - userdata[k]
        else:
            ret[k] = add
    return ret

import os
import sqlite3
def writre_recommend_to_sqlite(ret):
    db_filename = 'recommend.db'
    schema = """create table if not exists recommend
    (   id integer primary key autoincrement not null,
        username text,
        problem text
    )"""
    db_is_new = not os.path.exists(db_filename)
    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            print 'Creating schema.'
            conn.executescript(schema)
        cur = conn.cursor()
        print 'Insert data.'
        sql = """
            insert into recommend (username, problem)
            values (?, ?)
        """
        for k in ret:
            cur.execute(sql, (str(k), str(ret[k]).strip('set(').strip(')')))



if __name__ == '__main__':
    rules = process_rules('rules_20000_25000.data')
    userdata = process_user('poj20000_25000.data')
    ret = get_recommend(userdata, rules)
    #print '-' * 15, 'recommend', '-' * 15
    #fp = open('recommend.data', 'w')
    #for k in ret:
    #    fp.write(str(k) + ' ' + str(ret[k]) + '\n')
    #    print k, ' : ', ret[k]
    writre_recommend_to_sqlite(ret)

