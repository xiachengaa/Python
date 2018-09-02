# -*- coding:utf-8 -*-

import xlrd
import os
from config import *
import sys
import time
import socket
import codecs
import chardet

reload(sys)
sys.setdefaultencoding('utf8')


def resolve_excel_to_strings(filepath, result_dir, ori_key_list):
    xlrd.Book.encoding = "utf-8"
    data = xlrd.open_workbook(filepath)
    string_table = data.sheet_by_name(TABLENAME)
    key_table = data.sheet_by_name('mapping')
    place_col_number = get_number_in_row(string_table, PLACEHOLDERLANGUAGE, TITLELINE)
    place_holder_col_list = string_table.col_values(place_col_number)
    for lan_name, dir_name in PATHDIC.items():
        print "%s resolving..." % lan_name
        resolve_single_language(key_table, string_table, lan_name, dir_name,
                                place_holder_col_list, result_dir, ori_key_list)


# 处理一种语言
def resolve_single_language(key_table, string_table, language, file_path, place_holder_col_list,
                            result_dir, ori_key_list):
    key_list = []
    value_list = []
    language_col_number = get_number_in_row(string_table, language.strip(), TITLELINE)
    language_col_list = string_table.col_values(language_col_number)
    for key_value in ori_key_list:

        # key 为空或全是空格
        key = key_value.rstrip()
        if not key:  # key 是空格
            continue

        # 特殊key值处理
        if resolve_special_word(key):
            value = resolve_special_word(key)
            key_list.append(key)
            value_list.append(value)
            continue

        i = get_key_row_number(key_table, string_table, key)
        # 找不到对应的key值
        if not i:
            key_list.append(key)
            if key.find("//") > -1:  # 是注释
                value_list.append('++')
            else:
                value_list.append('--')    # 找不到此key
            continue

        value = language_col_list[i]
        if not value:
            value = place_holder_col_list[i]

        # 由于现在key值是从strings 文件中取得，故不需要对其进行下面的处理
        #        key = adjust_backslash_and_fit(key)
        #        key = adjust_double_quotation_and_fit(key)
        value = adjust_backslash_and_fit(value)
        value = adjust_double_quotation_and_fit(value)
        value = value.rstrip()
        # 找不到value值或全是空格
        if not value:
            print "找不到key对应的值或其对应的值为全为空格：%s" % key
            raise Exception("找不到key对应的值或其对应的值为全为空格,详见上边打印信息")
            continue
        key_list.append(key)
        value_list.append(value)

    if len(result_dir):
        file_path = ('%s/%s' % (result_dir, file_path))
    if not (os.path.exists(file_path)):
        os.mkdir(file_path)
    full_file_path = '%s/%s' % (file_path, STRING_FILE_NAME)
    write_file(key_list, value_list, full_file_path)


# 获取word在table表中row行中的序号,从0开始
def get_number_in_row(table, word, row):
    row_list = table.row_values(row)
    for i in xrange(0, len(row_list)):
        if word == row_list[i]:
            return i
    return False


# 获取word在table表中col列中的序号，从0开始
def get_number_in_col(table, word, col):
    col_list = table.col_values(col)
    for i in xrange(0, len(col_list)):
        if word == col_list[i]:
            return i
    return False


# 找到key在strings表所在的行
# key_table:mapping表  string_table:strings表  key_value：key值
def get_key_row_number(key_table, string_table, key_value):
    # 在mapping表中找到key值
    iID_col_num = get_number_in_row(key_table, 'iID', 0)
    id_row_num = get_number_in_col(key_table, key_value, iID_col_num)
    id_col_num = get_number_in_row(key_table, 'ID', 0)
    id_col_list = key_table.col_values(id_col_num)
    id_value = id_col_list[id_row_num]

    # 根据id_value找到在strings表中的行数
    id_col_num_in_strings = get_number_in_row(string_table, 'ID', TITLELINE)
    id_row_num_in_strings = get_number_in_col(string_table, id_value, id_col_num_in_strings)
    return id_row_num_in_strings


# 写入文件
def write_file(key_list, value_list, file_path):
    if len(key_list) != len(value_list):
        print 'values is not right for keys. something is wrong'
        return

    cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cur_host = socket.gethostname()
    cur_device = os.path.splitext(cur_host)[0]
    record_file = codecs.open(file_path, 'w', "utf-8")
    record_file.write('//创建时间：%s\n//设备：%s\n\n' % (cur_time, cur_device))
    try:
        for i in xrange(0, len(key_list)):
            key = key_list[i]
            value = value_list[i]
            if value == '--':
                record_file.write(('//Can\'t find Key in excel:\"%s\"\n' % (key)))
                continue
            if value == '++':
                record_file.write(('%s\n' % (key)))
                continue
            record_file.write(('\"%s\" = \"%s\";\n' % (key, value)))
    finally:
        record_file.close()

# #######异常符号处理#######


# 双引号处理
def adjust_double_quotation_and_fit(single_string):
    index = single_string.find(DOUBLE_QUOTATION)
    if index > -1:
        new_str = single_string.replace(DOUBLE_QUOTATION, COMP_DOUBLE_QUOTATION)
        return new_str
    return single_string


# 反斜杠处理
def adjust_backslash_and_fit(single_string):
    index = single_string.find(BACKSLASH)
    if index > -1:
        new_str = single_string.replace(BACKSLASH, COMP_BACKSLASH)
        return new_str
    return single_string


# 特殊字段处理
def resolve_special_word(a_string):
    if a_string == u"中国服务区":
        return u"中国服务区"
    if SPECIAL_WORD_LIST.has_key(a_string):
        return SPECIAL_WORD_LIST.get(a_string)
    return False


# #######异常符号处理#######


# ######特殊处理##########


# 获取文件编码格式
def get_file_encode_format(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    # TD 有精确度参数，后面可以判断一下，这里不影响
    format_str = chardet.detect(data)['encoding']
    f.close()
    return format_str


# 从strings 文件中读出一行后，获取其key值
def get_key_for_line(line_text):
    split_list = line_text.split('=')
    return split_list[0]


# 从strings 文件中获取key列表
def get_key_list_from_string_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    key_list = []
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    for line in file_handle:
        key = ""
        if line.find("=") > -1:
            key = eval(get_key_for_line(line))
        elif line.find("//") > -1:
            key = line.strip()
        if len(key) > 0:
            key_list.append(key)

    return key_list


# ######特殊处理##########


def main():
    excel_path = raw_input('请输入EXCEL文件路径：')
    excel_path = excel_path.strip()
    string_file_path = raw_input('请输入String文件路径：')
    string_file_path = string_file_path.strip()
    up_dir, basename = os.path.split(excel_path)
    result_dir = os.path.join(up_dir, 'result')
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    ori_key_list = get_key_list_from_string_file(string_file_path)
    if len(ori_key_list) < 4:
        print '从strings 文件中获取key列表失败'
        raise Exception("从strings 文件中获取key列表失败")
    resolve_excel_to_strings(excel_path, result_dir, ori_key_list)
    print "Competed ！"


if __name__ == '__main__':
    main()
