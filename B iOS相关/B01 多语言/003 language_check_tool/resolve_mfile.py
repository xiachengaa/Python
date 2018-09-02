# -*- coding: utf-8 -*-

import os
from config import *
from common_tool import *
import commands

default_config()

STRING_TEMP_DIR = "temp/mfile"


def get_string_file(project_path):
    if not os.path.exists(os.path.join(project_path, TEMP_DIR)):
        os.mkdir(os.path.join(project_path, TEMP_DIR))
    if not os.path.exists(os.path.join(project_path, STRING_TEMP_DIR)):
        os.mkdir(os.path.join(project_path, STRING_TEMP_DIR))

    get_string_cmd = "cd %s;" \
                     "find ./EZViewer -name *.m -print0 | xargs -0 genstrings -o %s" \
                      % (project_path, STRING_TEMP_DIR)
    (status, output) = commands.getstatusoutput(get_string_cmd)
    # TODO：判断输出，是否有不符合条件的输出
    if output.count("Bad entry in file") > 0:
        print output
        raise TypeError(".m文件中含有非法使用NSLocalizedString方法错误，请看上边打印结果")

    NORMAL_LOG("status:%s output:%s" % (status, output))


def get_key_list(project_path):
    localized_string_file_path = "%s/Localizable.strings" % (STRING_TEMP_DIR)
    if not os.path.exists(os.path.join(project_path, localized_string_file_path)):
        raise TypeError("生成m文件键名表失败")
    file_path = os.path.join(project_path, localized_string_file_path)
    key_list = get_key_list_from_string_file(file_path)
    return key_list


# 从strings 文件中读出一行后，获取其key值
def get_key_for_line(line_text):
    split_list = line_text.split('=')
    return split_list[0]


# 从strings 文件中获取key列表
def get_key_list_from_string_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    key_list = []
    line_num = 0;
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    for line in file_handle:
        line_num = line_num + 1
        key = ""
        if line.find("=") > -1:
            key = get_value_in_quote(get_key_for_line(line))
        else:
            continue

        if len(key) > 0:
            item = get_item_for_key(key, file_path, line_num)
            key_list.append(item)

    return key_list


# 对外接口
def get_mfile_key_list(project_path):
    get_string_file(project_path)
    return get_key_list(project_path)

