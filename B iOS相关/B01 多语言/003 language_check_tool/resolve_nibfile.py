# -*- coding: utf-8 -*-

from config import *
import os
import shutil
import commands
from common_tool import *
from check_leading import check_leading_in_file

default_config()

NIB_TEMP_DIR = "%s/nibTemp" % TEMP_DIR


def get_nib_string_file(project_path):
    for root, dirs, files in os.walk(project_path):
        if not contains_str(root, "ios/EZViewer"):
            continue
        for a_file in files:
            extension = os.path.splitext(a_file)[1]
            if extension == ".xib" or extension == ".storyboard":
                check_leading_in_file(os.path.join(root, a_file))
                if not generate_storyboard_string_file(project_path,
                                                       os.path.join(root, a_file),
                                                       a_file):
                    raise TypeError("从%s文件中提取key值失败" % a_file)


def generate_storyboard_string_file(project_path, storyboard_path, storyboard_name):

    pure_file_name = os.path.splitext(storyboard_name)[0]
    temp_string_file_name = "%s_string.strings" % pure_file_name
    nib_temp_dir = os.path.join(project_path, NIB_TEMP_DIR)
    temp_string_path = os.path.join(nib_temp_dir, temp_string_file_name)
    cmdstring = 'ibtool ' + storyboard_path + \
                ' --generate-strings-file ' + temp_string_path
    (status, output) = commands.getstatusoutput(cmdstring)
    if status == 0:
        return True
    else:
        ERROR_LOG(output)
        return False


def get_nib_key_list(project_path):
    nib_key_list = []
    for root, dirs, files in os.walk(os.path.join(project_path, NIB_TEMP_DIR)):
        for a_file in files:
            if os.path.splitext(a_file)[1] == ".strings":
                file_path = os.path.join(root, a_file)
                a_file_key_list = get_key_list_from_string_file(file_path)
                nib_key_list.extend(a_file_key_list)
    return nib_key_list


# 从strings 文件中获取key列表
def get_key_list_from_string_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    key_list = []
    line_num = 0
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    for line in file_handle:
        line_num = line_num + 1
        key = ""
        if line.find("=") > -1 and line.find("/* Class") == -1:
            key = get_value_in_quote(get_key_for_line(line))
        else:
            continue
        if len(key) > 0:
            item = get_item_for_key(key, file_path, line_num)
            key_list.append(item)
    return key_list


# 从strings 文件中读出一行后，获取其key值
def get_key_for_line(line_text):
    split_list = line_text.split('=')
    ori_str = split_list[1]
    # 去掉最后分号
    result = ori_str[:-2]
    return result


# 创建临时文件夹
def create_temp_dir(project_path):
    nib_temp_dir = os.path.join(project_path, NIB_TEMP_DIR)
    if os.path.exists(nib_temp_dir):
        shutil.rmtree(nib_temp_dir)
    temp_dir = os.path.join(project_path, TEMP_DIR)
    if not os.path.exists(temp_dir):
        os.mkdir(os.path.join(project_path, TEMP_DIR))
    os.mkdir(os.path.join(project_path, NIB_TEMP_DIR))


# 对外接口
def get_nibfile_key_list(project_path):
    create_temp_dir(project_path)
    get_nib_string_file(project_path)
    return get_nib_key_list(project_path)