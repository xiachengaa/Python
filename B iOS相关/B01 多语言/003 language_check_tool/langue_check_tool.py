# -*- coding: utf-8 -*-

from config import *
from resolve_mfile import get_mfile_key_list
from resolve_nibfile import get_nibfile_key_list
from resolve_stringfile import get_language_dic
from common_tool import *
import sys
import os
import shutil

default_config()

'''
实现思路：
一、leading/trailing 校验。遍历storyboard、xib，如果出现leading或trailing字段则报错
二、多语言校验
1、.m文件中使用到NSLocalizedString的key收集及解析出对应的key
2、.storyboard、.xib文件中字段收集及解析出对应的key
3、将.string文件解析成字典的形式
4、遍历两个key数组，如果在字典中找不到对应的key，则直接报错。
'''


def check_language(project_path):
    mfile_key_list = get_mfile_key_list(project_path)
    nibfile_key_list = get_nibfile_key_list(project_path)
    all_key_list = mfile_key_list + nibfile_key_list
    all_lan_dic = get_language_dic(project_path)
    # print "LLLL:nibKey:%d mfileKey:%d allKey:%d" % (len(nibfile_key_list), len(mfile_key_list), len(all_key_list))
    for item in all_key_list:
        key = parse_item(item)
        # print key
        for lan_key, lan_dic in all_lan_dic.items():
            if key not in lan_dic:
                if key in IGNORE_KEY_LIST:
                    NORMAL_LOG("Normal:ignore key:%s" % key)
                    continue
                # ERROR_LOG("WARNING(%s):%s" % (lan_key, key))
                print_item(item)
                # 正式时把这里放开，如果有找不到对应key的情况，直接报错。
                raise TypeError("(%s):%s" % (lan_key, key))
            else:
                NORMAL_LOG("Normal:%s" % key)
                continue


def clear_files(project_path):
    # 如果要找印详细错误信息，则不删除过程文件
    if config.DEBUG:
        return
    temp_dir = os.path.join(project_path, TEMP_DIR)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def main():

    if TEST_FLAG:
        check_language(TEST_PATH)
        clear_files(TEST_PATH)
    else:
        if len(sys.argv) > 1:
            check_language(sys.argv[1])
            clear_files(sys.argv[1])
            print "no issue found"
        else:
            raise TypeError("缺少地址参数")


if __name__ == '__main__':
    main()
