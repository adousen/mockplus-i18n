# -*- coding: utf-8 -*-
import sys


def is_valid_line(line):
    if line.startswith(';') or line.strip() == '':
        return False
    return True


def get_parts(line):
    if not is_valid_line(line):
        return
    li = line.split('=', 1)
    if len(li) != 2:
        raise Exception("wrong line", line)
    k, v = li
    return (k, v)


def check_file(p):
    '''
    校验文件是否合法
    1. 是否是用逗号分隔开的两个部分
    '''
    with open(p, 'r') as f:
        line = f.readline()
        while line:
            try:
                get_parts(line)
            except Exception, e:
                print e
                return False
            line = f.readline()
    return True


def check_file_struture(p1, p2):
    lines1 = get_lines(p1)
    lines2 = get_lines(p2)
    has_error = False
    idx = 1
    for s in lines1:
        for s2 in lines2:
            if s[0] == s2[0]:
                v1 = s[1]
                v2 = s2[1]
                res = has_the_same_struture(v1, v2)
                if res:
                    print '%d. [%s] %s \nCN ==> %sEN ==> %s' %(idx, s[0], res, v1, v2)
                    has_error = True
                    idx += 1
                break
    return has_error


def get_lines(p):
    lines = []
    with open(p, 'r') as f:
        line = f.readline()
        while line:
            if is_valid_line(line):
                ps = get_parts(line)
                if ps:
                    lines.append(ps)
            line = f.readline()
    return lines


def merge(src, dst, save_to):
    if not check_file(src):
        return
    if not check_file(dst):
        return
    if not check_file_struture(src, dst):
        return
    slines = get_lines(src)
    dlines = get_lines(dst)
    to_append = []
    for s in slines:
        found = False
        for s2 in dlines:
            if s[0] == s2[0]:
                Found = True
        if not found:
            to_append.append(s)


def has_the_same_struture(s1, s2):
    '''
    两个字符串的结构相同
    '''
    if len(s1.split('%')) != len(s2.split('%')):
        return '疑似转义字符不一致'
    # if len(s1.split('\\r\\n')) != len(s2.split('\\r\\n')):
        # return '疑似换行不一致'
    return ''


if __name__ == "__main__":
    src = './langs/zh-CN.txt'
    dst = './langs/jp.txt'
    save_to = './output/jp.txt'
    merge(src, dst, save_to)
