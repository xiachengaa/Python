# -*- coding:utf-8 -*-

import re
import xlrd
import os
import codecs
from config import *
import sys
import time
import socket
import codecs
import chardet
reload(sys)
sys.setdefaultencoding('utf8')



DOUBLE_QUOTATION = u'\"'
COMP_DOUBLE_QUOTATION = u'\\\"'
BACKSLASH = u'\\'
COMP_BACKSLASH = u'\\\\'

def resolve_excel_to_strings(filePath, result_dir, ori_key_list):
    xlrd.Book.encoding = "utf-8"
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(TABLENAME)
    key_table = data.sheet_by_name('mapping')
    # 取第一列数据，作为key
    key_col_number = get_number_in_row(table, KEYTITLE, TITLELINE)
    key_col_list = table.col_values(key_col_number)
    place_col_number = get_number_in_row(table, PLACEHOLDERLANGUAGE, TITLELINE)
    place_holder_col_list = table.col_values(place_col_number)
#    print place_holder_col_list
#    print key_col_list
    # print PATHDIC
    for lan_name, dir_name in PATHDIC.items():
        # print 'lan:%s , filepath:%s' % (key, value)
        resolve_single_language(key_table,table, key_col_list, lan_name, dir_name, place_holder_col_list, result_dir, ori_key_list)


# 处理一种语言
def resolve_single_language(key_table,table, key_col_list, language, file_path, place_holder_col_list, result_dir, ori_key_list):
    key_list = []
    value_list = []
    language_col_number = get_number_in_row(table, language.strip(), TITLELINE)
    language_col_list = table.col_values(language_col_number)
    key_col_number = get_number_in_row(table, KEYTITLE, TITLELINE)
#    print 'KEYLIST=========='
#    print ori_key_list
#    print 'KEYLIST=========='
    for key_value in ori_key_list:
    #找到key所在的行
#        i = get_number_in_col(table,key_value, key_col_number)
        if resolve_special_word(key_value):
#            print '中国服务区2: key %s====' % (key_value)
            value = resolve_special_word(key_value)
#            print '中国服务区2: value %s====' % (value)
            key_list.append(key_value)
            value_list.append(value)
            continue
        
        i = get_key_row_number(key_table,table,key_value)
        if not i:
#            print 'Can\'t find key:%s' % (key_value)
            key_list.append(key_value)
            if key_value.find("//") > -1:
                value_list.append('++')
            else:
                value_list.append('--')
            continue
        key = key_value.rstrip()
        if not key:
            continue
        value = language_col_list[i]
        if not value:
            value = place_holder_col_list[i]
        if not value:
#            print 'SPECIAL:not found for key: %s' % (key)
            continue
#        key = adjust_backslash_and_fit(key)
#        key = adjust_double_quotation_and_fit(key)
        value = adjust_backslash_and_fit(value)
        value = adjust_double_quotation_and_fit(value)
        value = value.rstrip()
        key_list.append(key)
        value_list.append(value)

    if len(result_dir):
        file_path = ('%s/%s' % (result_dir, file_path))

    if not (os.path.exists(file_path)) :
        os.mkdir(file_path)

    full_file_path = '%s/%s' % (file_path, STRING_FILE_NAME)
#    print 'write file===='
#    print value_list
    write_file(key_list, value_list, full_file_path)


# 获取word在table表中row行中的序号,从0开始
def get_number_in_row(table, word, row):
    row_list = table.row_values(row)
    # print row_list
    for i in xrange(0, len(row_list)):
        if word == row_list[i] :
#            print '列数%d' % (i)
            return i
#    print 'get_in_row:SPECIAL:%s' % (word)
#    print '在 %i 行找不到值 %s ' % (row, word)
#    raise Exception('找不到关键词')
    return False


# 获取word在table表中col列中的序号，从0开始
def get_number_in_col(table, word, col):
    col_list = table.col_values(col)
#    print 'col_list========='
#    print col_list
#    print 'col_list========='
    for i in xrange(0, len(col_list)):
        if word == col_list[i] :
            return i
#    print '在 %f 列找不到值 %s ' % (col, word)
#    print 'get_in_col:SPECIAL:%s' % (word)
#    raise Exception('找不到关键词')
    return False

#找到key在strings表所在的行
#key_table:mapping表  string_table:strings表  key_value：key值
def get_key_row_number(key_table,string_table,key_value):
#在mapping表中找到key值
    iID_col_num = get_number_in_row(key_table,'iID',0);
    id_row_num = get_number_in_col(key_table,key_value,iID_col_num)
    id_col_num = get_number_in_row(key_table,'ID',0)
    id_col_list = key_table.col_values(id_col_num)
    id_value = id_col_list[id_row_num]

#根据id_value找到在strings表中的行数
    id_col_num_in_strings = get_number_in_row(string_table,'ID',TITLELINE)
    id_row_num_in_strings = get_number_in_col(string_table,id_value,id_col_num_in_strings)
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
        for i in xrange(0,len(key_list)):
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
#    print single_string
    index = single_string.find(DOUBLE_QUOTATION)
    if index > -1:
        new_str = single_string.replace(DOUBLE_QUOTATION,COMP_DOUBLE_QUOTATION)
#        print 'newStr:%s' % (new_str)
        return new_str
    return single_string

#反斜杠处理

def adjust_backslash_and_fit(single_string):
    index = single_string.find(BACKSLASH)
#    print single_string
    if index > -1:
        new_str = single_string.replace(BACKSLASH,COMP_BACKSLASH)
#        print 'newStr:%s' % (new_str)
        return new_str
    return single_string

#特殊字段处理
def resolve_special_word(a_string):
    if a_string == u"中国服务区":
       return u"中国服务区"
    if SPECIAL_WORD_LIST.has_key(a_string):
        return SPECIAL_WORD_LIST.get(a_string)
    return False



########异常符号处理#######


#######字符处理##########

def get_file_encode_format(file_path):
    f = open(file_path,'rb')
    data = f.read()
    #TD 有精确度参数，后面可以判断一下
    format_str = chardet.detect(data)['encoding']
    f.close()
    return format_str

def get_key_for_line(line_text):
    step1List = line_text.split('=')
    return step1List[0]

def get_key_list_from_string_file(file_path):
    if not os.path.isfile(file_path.strip()):
        raise TypeError(file_path + " does not exist")
    key_list = []
    file = codecs.open(file_path,'r',get_file_encode_format(file_path))
    for line in file:
        key = ""
        if line.find("=") > -1:
            key = eval(get_key_for_line(line))
        elif line.find("//") > -1:
            key = line.strip()
        if len(key) > 0:
            key_list.append(key)

    return key_list

#######字符处理##########



def main():
    excel_path = raw_input('请输入EXCEL文件路径：')
    excel_path = excel_path.strip()
    string_file_path = raw_input('请输入String文件路径：')
    string_file_path = string_file_path.strip()
    # result_dir = raw_input('请输入结果存放路径：')
    up_dir, basename = os.path.split(excel_path)
    result_dir = os.path.join(up_dir, 'result')
#    print result_dir
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    ori_key_list = get_key_list_from_string_file(string_file_path)
    if len(ori_key_list) < 4:
#        print 'no keys'
        return
#    print key_list
    resolve_excel_to_strings(excel_path, result_dir, ori_key_list)
    print 'Completed!'

if __name__ == '__main__':
    main()





