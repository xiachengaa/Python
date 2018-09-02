# -*- coding: utf-8 -*-

import codecs
import chardet
import imp
import sys
import re
import config


def default_config():
    imp.reload(sys)
    sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的


# 获取文件编码格式
def get_file_encode_format(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    # TD 有精确度参数，后面可以判断一下，这里不影响
    format_str = chardet.detect(data)['encoding']
    f.close()
    return format_str


# 是否包含某个字符串
def contains_str(ori_str, a_str):
    ori_str_low = ori_str.lower()
    a_str_low = a_str.lower()
    if a_str_low in ori_str_low:
        return True
    else:
        return False


# 获取字典中某一个value对应的key值
def get_key_for_value(dic, a_value):
    for key, value in dic.items():
        if value == a_value:
            return key

    return False


def get_value_in_quote(text):
    pattern = re.compile('"(.*)"')
    res_list = pattern.findall(text)
    if len(res_list) >= 1:
        return res_list[0]
    else:
        print "WARNING:text:%s" % text
        raise Exception(".string多语言文件中有换行符或空值")


# 根据key、file、line生成调试字典
def get_item_for_key(key, file_path, line_num):
    if config.DEBUG:
        return {config.ERR_FILE_KEY: file_path, config.ERR_LINE_KEY: line_num, config.ITEM_KEY: key}
    else:
        return key


# 根据数组中的item 取出key值
def parse_item(item):
    if config.DEBUG:
        return item[config.ITEM_KEY]
    else:
        return item


# 打印item
def print_item(item):
    if config.DEBUG:
        print "Error File:%s, Line:%s key:%s" % (item[config.ERR_FILE_KEY],
                                                 item[config.ERR_LINE_KEY], item[config.ITEM_KEY])


def WARNGIN_LOG(text):
    print text
    return


def ERROR_LOG(text):
    print text
    # return


def NORMAL_LOG(text):
    # print text
    return
