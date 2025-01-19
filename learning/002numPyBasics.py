# -*- coding = utf-8 -*-
# @Time: 2024/10/15 14:21
# @Author: Zhihang Yi
# @File: 002numPyBasics.py
# @Software: PyCharm

import numpy


def main():
    # 可以用.shape对数组的形状直接进行改变。
    a = numpy.arange(10)
    print(a.shape, a, sep=':\n')
    a.shape = (5, 2)
    print(a.shape, a, sep=':\n')
    a.shape = (5, 2, 1)
    print(a)

    # 也可以使用reshape()函数直接进行更改。
    a = numpy.arange(10).reshape(5, 2)
    print(a)
    a = numpy.arange(10).reshape(5, 2, 1)
    print(a)

    # 对数组更改类型需要用....astype('...')。
    # 不能直接用 a.dtype = '...' 这种方式进行更改，会出错。
    a = a.astype(float)
    print(a.dtype, a, sep=':\n')

    # .size得到数组的个数，len()的用法和Python语法一样。
    print('size: ' + str(a.size) + '\n' + 'rows: ' + str(len(a)))

    # 可以用一般的访问列表的方法来访问ndarray。
    print(a[4][1][0])
    # 或者用a[..., ...]的方式来访问(这是ndarray独特的访问方式)。
    print(a[4, 1, 0])

    # ndarray在循环中的遍历：
    b = numpy.arange(30)
    b.shape = (3, 2, 5)
    print(b)
    # 由于b.shape是元组，所以可以用[...]的方式得到第...个数字。
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                if i == b.shape[0] - 1 and j == b.shape[1] - 1 and k == b.shape[2] - 1:
                    print(b[i, j, k])
                else:
                    print(b[i, j, k], end=', ')

    # numpy.array()中也可以传入一个列表。
    data = [
        ['Alice', [114, 137, 142], 'Chongqing'],
        ['Bob', [112, 127, 131], 'Chengdu'],
        ['Dennis', [97, 113, 127], 'Guangzhou'],
        ['Eric', [137, 147, 143], 'Hebei']
    ]
    # 传入的时候一定要加上dtype=object，将data当作一个对象传入numpy.array()，否则会报错。
    data = numpy.array(data, dtype=object)
    print(data)
    print(data[0][1][0])
    # 注意不能用data[0, 1, 0]的方式访问，因为实际上data是一个二位的ndarray。
    print(data[0, 1][0])

    # .ndim得到ndarray的维度，以整型的方式返回。
    # .shape得到ndarray的每个维度的个数，以元组的方式返回。
    # .dtype得到ndarray中元素的类型。


if __name__ == '__main__':
    main()
