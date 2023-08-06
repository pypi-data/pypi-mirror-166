import os
import sys

'''
可执行命令所在的根文件夹
开发环境: /Users/code/msds/
全局环境: /Library/Frameworks/Python.framework/Versions/3.10/
'''
PATH_ROOT = os.path.join(sys.path[0], '../')

'''
全局，可执行命令对应的资源文件地址: /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages
'''
PATH_SOURCE = sys.path[-2]
