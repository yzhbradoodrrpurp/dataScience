# -*- coding = utf-8 -*-
# @Time: 2024/10/19 16:17
# @Author: Zhihang Yi
# @File: 005DataFramePandas.py
# @Software: PyCharm

import pandas as pd
import random

"""
DataFrame是一个二维数据，类似于电子表格或者数据库表。
"""

# DataFrame中接收一个字典，字典的键是列索引。列索引是必须有的。
# DataFrame中的一个列中的数据必须是同一个类型。
a = pd.DataFrame({'one': [1, 2, 3], 'two': [4, 5, 6]})
print(a)

# DataFrame中的字典也可以接收Series，这样的话，每一列的个数可以不同并且索引也可以不同。
x = pd.Series([random.randint(-10, 10) for i in range(20)])
y = pd.Series(random.randint(-5, 5) for i in range(15))
c = pd.DataFrame({'one': x, 'two': y})
print(c)
d = pd.DataFrame({'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']), 'two': pd.Series([1, 2], index=['x', 'y'])})
print(d)

# .index, .columns, .values是DataFrame的属性，index返回其行索引，columns返回列索引，values返回值(值组成的ndarray)。
print(d.index)
print(d.columns)
print(d.values)

# .T得到DataFrame数据的转置，行索引和列索引也会变换位置。
print(d.T)

# .describe()可以得到一个DataFrame类型数据每一行的统计信息。
print(d.describe())

"""
CSV（Comma-Separated Values）是一种用于存储表格数据的文件格式，数据以逗号分隔。
每一行代表一条记录，行中的字段通过逗号分隔。
CSV 文件通常用于数据交换，易于读取和写入，适用于电子表格、数据库和数据分析等应用。

e.g.:
name,age,city
Alice,30,New York
Bob,25,Los Angeles
这里的第一行是列名，后面的行是具体的数据记录。
"""

# DataFrame可以通过pd.read_csv('...')读取一个csv文件并创建一个DataFrame数据。
a = pd.read_csv('005test.csv')
print(a)

# 我们也可以用a.to_csv('...')将DataFrame类型的数据a保存为csv格式的文件。
x = pd.Series([random.randint(-10, 10) for i in range(20)])
y = pd.Series(random.randint(-5, 5) for i in range(15))
d = pd.DataFrame({'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']), 'two': pd.Series([1, 2], index=['x', 'y'])})
d.to_csv('005test1.csv')

# 想要得到DataFrame中的某一个值，需要先对列进行索引，然后再对行进索引。
x = pd.Series([random.randint(-10, 10) for i in range(20)])
y = pd.Series(random.randint(-5, 5) for i in range(15))
d = pd.DataFrame({'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']), 'two': pd.Series([1, 2], index=['x', 'y'])})
print(d['one']['a'])
# 或者使用loc[], iloc[]，这个时候就是先对行进行索引，然后再对列进行索引。
print(d.loc['a', 'one'])

# DataFrame类型数据在进行加减乘除操作时也是根据行索引、列索引进行对齐的。
a = pd.DataFrame({'one': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']), 'two': pd.Series([1, 2], index=['x', 'y'])})
b = pd.DataFrame({'two': pd.Series([2, 3], index=['y', 'x']), 'one': pd.Series([1, 2, 3, 4], index=['b', 'd', 'c', 'a'])})
c = a + b
print(c)

# 可以用.isnull(), notnull()判断DataFrame中某个位置的数据是不是NaN。
print(c.notnull(), c.isnull())

# 对DataFrame类型也能使用.dropna()方法去掉NaN。
# 对how可以传入any/all。any表示去除只要出现了NaN的行，all表示去除全都是NaN的行。默认是any。
print(c.dropna(how='any'), c.dropna(how='all'))
# 可以对特定的轴进行删除，axis默认是0，即对行进行删除。可以修改为axis为1，即对列进行删除。
print(c.dropna(axis=1, how='any'))

# 也可以使用.fillna(...)给NaN赋值。
print(c.fillna(0))

# .mean()求平均，默认按列求平均，设定axis=1按行求平均。
# .sum()求和，默认按列求和，设定axis=1按行求平均。
print(d.sum(), d.sum(axis=1))
print(d.mean, d.mean(axis=1))

# .sort_values()可以对DataFrame进行排序，by表示通过哪一个列进行排序，ascending表示是否进行升序。
# 如果参与排序的那一列有NaN，则NaN统一放在最后面。
a = pd.DataFrame({'one': pd.Series([random.randint(-10, 10) for i in range(10)]), 'two': pd.Series([random.randint(-10, 10) for i in range(10)])})
print(a)
print(a.sort_values(by='one', ascending=True))
print(a.sort_values(by='two', ascending=False))

