# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_leading
   Description :  what's the purpose of the file?
   Author :       xiacheng
   date：         2017:12:26 16:04
-------------------------------------------------
"""
import os

from common_tool import *
from config import *
default_config()


# 检查nib文件中是否有leading和trailing
def check_leading_in_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    error_flag = False
    for line in file_handle:
        if line.find("leading") > -1 or line.find("trailing") > -1:
            error_flag = True
    if error_flag:
        # TODO: 这里控制有leading和trailing时要不要报错。
        raise TypeError(file_path + " has leading or trailing in file")
        # print "Error: %s" % file_path
    else:
        NORMAL_LOG("%s is fine" % file_path)
