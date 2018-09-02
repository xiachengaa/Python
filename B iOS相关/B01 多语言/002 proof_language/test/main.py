# -*- coding:utf-8 -*-

import re
import xlrd
import os
import codecs
from config import *
import sys
import time
import socket
reload(sys)
sys.setdefaultencoding('utf8')



DOUBLE_QUOTATION = u'\"'
COMP_DOUBLE_QUOTATION = u'\\\"'
BACKSLASH = u'\\'
COMP_BACKSLASH = u'\\\\'

def resolve_excel_to_strings(filePath, result_dir):
    xlrd.Book.encoding = "utf-8"
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(TABLENAME)
    # 取第一列数据，作为key
    key_col_number = get_number_in_row(table, KEYTITLE, TITLELINE)
    key_col_list = table.col_values(key_col_number)
    place_col_number = get_number_in_row(table, PLACEHOLDERLANGUAGE, TITLELINE)
    place_holder_col_list = table.col_values(place_col_number)
#    print place_holder_col_list
    print key_col_list
    # print PATHDIC
    for lan_name, dir_name in PATHDIC.items():
        # print 'lan:%s , filepath:%s' % (key, value)
        resolve_single_language(table, key_col_list, lan_name, dir_name, place_holder_col_list, result_dir)


# 处理一种语言
def resolve_single_language(table, key_col_list, language, file_path, place_holder_col_list, result_dir):
    key_list = []
    value_list = []
    language_col_number = get_number_in_row(table, language.strip(), TITLELINE)
    language_col_list = table.col_values(language_col_number)
    # 读取每一行对应的数据,从第二行开始
    for i in xrange(1, table.nrows):
        key = key_col_list[i]
        if not key:
            continue
        value = language_col_list[i]
        if not value:
            value = place_holder_col_list[i]
        if not value:
            print 'placeholder language is not found,something is wrong.key: %s' % (key)
            raise Exception('找不到占位语言')
        key = adjust_backslash_and_fit(key)
        key = adjust_double_quotation_and_fit(key)
        value = adjust_backslash_and_fit(value)
        value = adjust_double_quotation_and_fit(value)
        if resolve_special_word(key):
            value = resolve_special_word(key)
        key_list.append(key)
        value_list.append(value)
        # print 'key:%s value:%s' % (key, value_list[i - 1])

    if len(result_dir):
        file_path = ('%s/%s' % (result_dir, file_path))

    if not (os.path.exists(file_path)) :
        os.mkdir(file_path)

    full_file_path = '%s/%s' % (file_path, STRING_FILE_NAME)
    write_file(key_list, value_list, full_file_path)


# 获取word在table表中row行中的序号,从0开始
def get_number_in_row(table, word, row):
    row_list = table.row_values(row)
    # print row_list
    for i in xrange(0, len(row_list)):
        if word == row_list[i] :
            print '列数%d' % (i)
            return i

    print '在 %i 行找不到值 %s ' % (row, word)
    raise Exception('找不到关键词' % word)


# 获取word在table表中col列中的序号，从0开始
def get_number_in_col(table, word, col):
    col_list = table.col_values(col)
    for i in xrange(0, len(col_list)):
        if word == col_list[i] :
            return i
    print '在 %f 列找不到值 %s ' % (col, word)
    raise Exception('找不到关键词')


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
        for i in xrange(0,len(key_list)):
            key = key_list[i]
            value = value_list[i]
            record_file.write(('\"%s\" = \"%s\";\n' % (key, value)))
    finally:
        record_file.close()

# # 把文本转化为字典
# def transTextToDictionary(text):
# #     分隔等号两边
# #     去双绰号及空格，然后返回
#     step1List = text.split('=')
#     for txt in step1List:
#         patter = re.compile('"([^"]+)"')
#         list = patter.findall(txt)
#         print list
#     return 1,1

########异常符号处理#######
#双引号处理
def adjust_double_quotation_and_fit(single_string):
    index = single_string.find(DOUBLE_QUOTATION)
    print single_string
    if index > -1:
        new_str = single_string.replace(DOUBLE_QUOTATION,COMP_DOUBLE_QUOTATION)
        print 'newStr:%s' % (new_str)
        return new_str
    return single_string

#反斜杠处理

def adjust_backslash_and_fit(single_string):
    index = single_string.find(BACKSLASH)
    print single_string
    if index > -1:
        new_str = single_string.replace(BACKSLASH,COMP_BACKSLASH)
        print 'newStr:%s' % (new_str)
        return new_str
    return single_string

#特殊字段处理
def resolve_special_word(a_string):
    if SPECIAL_WORD_LIST.has_key(a_string):
        return SPECIAL_WORD_LIST.get(a_string)
    return False



########异常符号处理#######



def main():
    excel_path = raw_input('请输入EXCEL文件路径：')
    excel_path = excel_path.strip()
    # result_dir = raw_input('请输入结果存放路径：')
    up_dir, basename = os.path.split(excel_path)
    result_dir = os.path.join(up_dir, 'result')
    print result_dir
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    resolve_excel_to_strings(excel_path, result_dir)
    print 'Completed!'

if __name__ == '__main__':
    main()





