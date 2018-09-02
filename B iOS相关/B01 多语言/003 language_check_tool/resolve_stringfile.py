# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     resolve_stringfile
   Description :  处理.strings文件，从中得到各种语言的键值对。
   Author :       xiacheng
   date：         2017:12:26 09:35
-------------------------------------------------
"""
import os
from config import *
from common_tool import *

'''
1、遍历对应文件夹，找到其语言的文件夹，然后根据文件夹名知道其对应的语言
2、读取strings文件，到其键值对。
'''


def get_all_language_dic(project_path):
    all_lan_dic = {}
    for root, dirs, files in os.walk(project_path):
        if not is_right_file(root):
            continue
        for a_file in files:
            if not (a_file == "Localizable.strings"):
                continue
            string_file_path = os.path.join(root, a_file)
            NORMAL_LOG("STIRNG_FILE_PATH:%s" % string_file_path)
            lan_key_dic = get_key_value_dic_from_string_file(string_file_path)
            dir_name = os.path.split(root)[1].strip()
            lan_key = get_key_for_value(PATHDIC, dir_name)
            all_lan_dic[lan_key] = lan_key_dic
    return all_lan_dic


# 是否是多语言文件夹 是否是多语言文件夹
def is_right_file(dir_path):
    # 如果是thirdLibrary里面的多语言文件则直接跳过
    if not contains_str(dir_path, "ios/EZViewer"):
        return False
    dir_name = os.path.split(dir_path)[1].strip()
    dir_name_list = PATHDIC.values()
    if dir_name in dir_name_list:
        return True
    else:
        return False


# 从strings 文件中读出一行后，获取其key值
def get_key_value_for_line(line_text):
    split_list = line_text.split('=')
    a = split_list[0]
    b = split_list[1]
    key = get_value_in_quote(split_list[0])
    value = get_value_in_quote(split_list[1])
    return key, value


# 从strings 文件中获取key列表
def get_key_value_dic_from_string_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    key_value_dic = {'test': "test"}
    key_value_dic.clear()
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    for line in file_handle:
        key = ""
        value = ""
        if line.find("=") > -1:
            (key, value) = get_key_value_for_line(line)
        else:
            continue

        if len(key) > 0:
            key_value_dic[key] = value
    NORMAL_LOG("DEBUG:file path: %s" % file_path)
    NORMAL_LOG("DEBUG:dic length:%d" % len(key_value_dic))
    return key_value_dic


# 返回一个字典，字典的key为语言名，value为对应语言的键值对
def get_language_dic(project_path):
    return get_all_language_dic(project_path)
