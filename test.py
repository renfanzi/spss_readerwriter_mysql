#!/usr/bin/env python
# -*- coding:utf-8 -*-

li = [
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['h', 'i', 'g']],
    [[11, 22, 33], [44, 55, 66], [77, 88, 99]]
]

a = li[0]
print(len(li))
for i in range(1, len(li)):
    for j in range(len(a)):
        a[j] += li[i][j]

print(a)
# [[1, 2, 3, 'a', 'b', 'c', 11, 22, 33], [4, 5, 6, 'd', 'e', 'f', 44, 55, 66], [7, 8, 9, 'h', 'i', 'g', 77, 88, 99]]
