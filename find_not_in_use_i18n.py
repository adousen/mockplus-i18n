# -*- coding: utf-8 -*-
import re

PATTERN = re.compile(r""".*i18n\.t[\(\s]+['\"](?P<key>[^'\"]*)['\"][\)\s]""", re.I)

def read_all_in_web():
    with open('./temp/all-in-js.txt', 'r') as f:
        lines = f.readlines()
    return (l.strip() for l in lines)


def read_all_in_use():
    in_use = []
    with open('./temp/i18n.log', 'r') as f:
        lines = f.readlines()
    ls = (l.strip() for l in lines)
    for l in ls:
        m = PATTERN.match(l)
        if m:
            gd = m.groupdict()
            key =  gd['key']
            if key not in in_use:
                in_use.append(key)
    return in_use


def get_not_in_use(all_keys, in_use):
    not_in_use = []
    for k in all_keys:
        if k not in in_use:
            not_in_use.append(k)
    return not_in_use


if __name__ == "__main__":
    all_keys = read_all_in_web()
    in_use =  read_all_in_use()
    not_in_use = get_not_in_use(all_keys, in_use)
    for l in not_in_use:
        print l

