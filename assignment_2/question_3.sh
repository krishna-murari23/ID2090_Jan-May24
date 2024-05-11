#!/bin/bash

python3 - "$@" <<END
import math
import sys

p1 = open(sys.argv[1], "r")
lines = p1.readlines()
L = lines[1:]
D = len(L)

d = 0
tf = 0

if len(sys.argv) > 2:
    a = sys.argv[2]
    l = []

    for i in L:
        x = i.replace(",", "").replace(".", "").replace("\n", "")
        l.append(x)

    for line in l:
        t1 = line.split(" ")
        t = t1[1:]

        if a in t:
            d = d + 1
            c = 0
            c1 = 0
            for x in t:
                if x == a:
                    c = c + 1
            c1 = len(t)
            tf = tf + (c / c1)

    idf = math.log2((D + 1) / (d + 1))
    tf_idf = (tf * idf) / D
    tf_idfT = "{:.4f}".format(tf_idf)
    print("{}".format(tf_idfT))

else:
    s = set()
    v = []
    l = []
    for i in L:
        x = i.replace(",", "").replace(".", "").replace("\n", "")
        l.append(x)

    for line in l:
        t1 = line.split(" ")
        t = t1[1:]
        s.update(t)

    for i in s:
        tf = 0
        d = 0
        a = i
        l = []

        for i in L:
            x = i.replace(",", "").replace(".", "").replace("\n", "")
            l.append(x)

        for line in l:
            t1 = line.split(" ")
            t = t1[1:]

            if a in t:
                d = d + 1
                c = 0
                c1 = 0
                for x in t:
                    if x == a:
                        c = c + 1
                c1 = len(t)
                tf = tf + (c / c1)

        idf = math.log2((D + 1) / (d + 1))
        tf_idf = (tf * idf) / D
        tf_idfT = "{:.4f}".format(tf_idf)
        v.append(tf_idfT)

    s = list(s)
    m1 = max(v)
    i1 = v.index(m1)
   
    print("{}, {}".format(s[i1], m1))
    v.remove(m1)
    del s[i1]
    m2 = max(v)
    i2 = v.index(m2)
    print("{}, {}".format(s[i2], m2))
    v.remove(m2)
    del s[i2]
    m3 = max(v)
    i3 = v.index(m3)
    print("{}, {}".format(s[i3], m3))
    v.remove(m3)
    del s[i3]
    m4 = max(v)
    i4 = v.index(m4)
    print("{}, {}".format(s[i4], m4))
    v.remove(m4)
    del s[i4]
    m5 = max(v)
    i5 = v.index(m5)
    print("{}, {}".format(s[i5], m5))
END
