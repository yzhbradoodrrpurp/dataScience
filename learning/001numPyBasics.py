# -*- coding = utf-8 -*-
# @Time: 2024/10/15 12:57
# @Author: Zhihang Yi
# @File: 001numPyBasics.py
# @Software: PyCharm

import numpy

def main():
    """
    在numpy中创建了一个ndarray数组，实际上会分两个部分去存储这个。

    第一部分是实际存储数组元素的部分，NumPy 将所有数组元素存储在一个连续的内存块中。
    无论数组是一维还是多维，所有数据都存储在一个线性内存区域，这种设计可以提高数组操作的效率。

    第二个部分是数组元数据，包含了.shape, .ndim, dtype, .data...
    这些都是数组的属性，可以直接调用。

    另外，ndarray实际上是一个同质数组，数组的所有元素都会强制转换为同类型(可以输入不同类型的元素，但是ndarray会强制进行类型转换)。
    """

    array1 = numpy.array([
        [1, 2, 3],
        [4, 5, 6]
    ])
    array1 = numpy.array([1, 2, 3, 4, 5, 6])
    array2 = [1, 2, 3, 4, 5, 6]
    # 区别一下numpy的列表(数组)和一般的列表。
    print(array1, type(array1), sep=': ')
    print(array2, type(array2), sep=': ')

    # .shape是一个属性，返回数组的维度，它会以一个元组的形式给出数组在每个维度上的大小。
    # (x,)表示是一行x列数组。(x, y)表示x行y列数组。
    print(array1.shape)

    # 可以通过修改.shape来修改数组的结构。
    # 前提是数组的个数必须与修改后的结构相符合，否则会报错。
    array1.shape = (2, 3)
    print(array1)
    array1.shape = (6,)
    print(array1)

    # 数组可以进行数值运算。
    # 数组里的每一个元素都乘3。
    array1 = array1 * 3
    print(array1)
    # //是整除。
    array1 = array1 // 3
    print(array1)

    # 可以将数组和常量进行比较，在对应的位置上返回一个bool类型变量。
    print(array1 > 3)

    # 两个数组相加，即在对应位置上的数字相加。
    # 要求两个数组是形状相同的，或者是能够通过“广播机制”转换为形状相同的。
    print(array1 + array1)

    # numpy创建ndarray的第二种方式，使用numpy.arange(..., ..., ...)
    # 第一个数表示起始数值，第二个数表示结束数值(不包括)，第三个数表示步长(隔几个元素添加一个元素)。
    # 在Python的语法中表示为range(... : ... : ...)
    array2 = numpy.arange(2, 14, 3)
    print(array2)
    # numpy.arange()中的起始数值和步长都可以省略，和Python标准语法的省略方式一样。
    array2 = numpy.arange(14)
    print(array2)
    array2 = numpy.arange(1, 6)
    print(array2)

    # 用numpy.zeros()可以指定数字x，然后创建一个有x个0的数组。
    array3 = numpy.zeros(6)
    print(array3)
    # 可以传入一个元组，指定生成的形状。
    # 还可以指定dtype，每一个0是什么类型的数据。
    array3 = numpy.zeros(shape=(2, 3), dtype=int)
    print(array3)

    # numpy.ones()的使用方法和numpy.zeros()一摸一样。
    array4 = numpy.ones(shape=(2, 3), dtype=int)

    # numpy.zeros_like(...)接收一个ndarray，然后得到一个形状为...的内容全为0的数组。
    array5 = numpy.zeros_like(array4)
    print(array5)

    # numpy.ones_like()的使用方式和numpy.zeros_like()一摸一样。
    array5 = numpy.ones_like(array4)
    print(array5)

    # numpy.linspace(2, 7, 10)指的是从2到7之间平均步长得到10个数(包括起始点2和终点7)。
    array6 = numpy.linspace(2, 7, 10).reshape(2, 5)
    print(array6)


if __name__ == '__main__':
    main()
