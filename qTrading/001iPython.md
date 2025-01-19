# 一.iPython:

# 1.iPython 相比于Python命令行具有多项优势：

    自动补全：IPython 支持智能自动补全(按下tab键)，帮助用户快速输入命令和变量。

    模糊查找：可以用 '*', '?' 进行模糊查找。
        e.g.:
            a = []  a.*app*? # 查找一个列表所有含有app的方法或者属性。  
                    a.*app? # 查找一个列表所有以app结尾的方法或者属性。
                    a.app*? # 查找一个列表所有以app开头的方法或者属性。

    查询函数的功能：在函数名后面加上 '?' 可以查询这个函数的相关信息，加上 '??' 得到更详细的信息。
        e.g.:
            a = []  a.append?  a.append??

    魔术命令：以 '%' 开头的就是魔术命令。
        e.g.: 
            %run FILENAME.py #可以运行一个Python文件(确保路径是正确，可用pwd查看)。
            %paste #可以直接将剪贴板的内容复制到iPython中并执行。
            %timeit #可以测试代码片段运行时间的长度。
            
            %bookmark NAME PATH 可以创建一个去到PATH的名，为NAME的bookmark。这样就可以直接 'cd NAME' 去到这个路径。
            %bookmark -l 可以查看你添加的所有的bookmark。
            %bookmark -d NAME 可以删除名为NAME的bookmark。
            %bookmark -r 可以删除所有的bookmark。

    可视化界面: 用 'pip install jupyter' 下载jupyter notebook.
   

    总结：
    iPython 提供了更强大和灵活的交互式编程体验，特别适合数据科学、机器学习和科研等领域的工作，能够显著提升工作效率。

# 2.在命令行中输入 'ipython' 直接进入ipython环境。

