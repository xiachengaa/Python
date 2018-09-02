# -*- coding:utf-8 -*-

import xlwt
import xlrd
from xlutils.copy import copy
from config import *
import os
import shutil
import time
from resolve_stringfile import *

strings_ID_col_num = 2
strings_aID_col_num = 1
strings_iID_col_num = 0
mapping_ID_col_num = 0
mapping_aID_col_num = 1
mapping_iID_col_num = 2


def generate_new_excel(excel_path):
    xlrd.Book.encoding = "utf-8"
    # 打开excel,并将此excel复制,方便后续写入
    excel_file_data = xlrd.open_workbook(excel_path)
    new_excel_file_data = copy(excel_file_data)

    # 两个table的值
    strings_table_date = excel_file_data.sheet_by_name(STRING_TABLE_NAME)
    mapping_table_date = excel_file_data.sheet_by_name(MAPPING_TABLE_NAME)
    and_table_date = excel_file_data.sheet_by_name("And")
    new_table_data = excel_file_data.sheet_by_name("new")
    new_sheet_wt = new_excel_file_data.get_sheet(3)
    # strings_table_date_wt = new_excel_file_data.get_sheet(1)

    # strings表中列
    strings_ID_col_data_list = strings_table_date.col_values(strings_ID_col_num)
    strings_aID_col_data_list = strings_table_date.col_values(strings_aID_col_num)
    strings_iID_col_data_list = strings_table_date.col_values(strings_iID_col_num)

    # mapping表中列
    mapping_ID_col_data_list = mapping_table_date.col_values(mapping_ID_col_num)
    mapping_aID_col_data_list = mapping_table_date.col_values(mapping_aID_col_num)
    mapping_iID_col_data_list = mapping_table_date.col_values(mapping_iID_col_num)

    #And 表中的列
    and_aID_col_data_list = and_table_date.col_values(0)

    # new 表中的列
    new_iID_col_data_list = new_table_data.col_values(1)

    # string_dic = get_key_value_dic_from_string_file(STRING_FILE_PATH)
    # value_list = string_dic.values()
    # print len(value_list)

# iOS有安卓没有
    # count = 0
    # for i in xrange(0, len(value_list)):
    #     key_str_value_zh = value_list[i].strip()
    #     string_row_num = get_number_in_col(new_table_data, key_str_value_zh, 4)
    #     if not string_row_num:
    #         print "value-zh:%s" % key_str_value_zh
    #         count+=1

#从strings文件找value对应的key值
    string_dic = get_key_value_dic_from_string_file(STRING_FILE_PATH)
    print len(new_iID_col_data_list)
    count = 0
    for i in xrange(0, len(new_iID_col_data_list)):
        key_str_iID = new_iID_col_data_list[i].strip()
        # 判断需要更正
        if len(key_str_iID) == 0 or key_str_iID == "/" or key_str_iID == "\\":
            # 找到简体中文
            zh_key_str = new_table_data.cell(i, 4).value
            aID_key_str = new_table_data.cell(i, 0).value
            # # 与mapping表中的iID列中找到对应
            # mapping_row_num = get_number_in_col(mapping_table_date, zh_key_str, 2)
            # if not mapping_row_num:
            #     print "在mapping中找不到:key:%s aID:%s" % (zh_key_str, aID_key_str)
            #     count+=1
            #     continue
            # 去string文件中找到对应的值
            iID = get_key_for_string(string_dic, zh_key_str)
            if not iID:
                print "在mapping中找不到:key:%s aID:%s" % (zh_key_str, aID_key_str)
                count+=1
                continue
            new_sheet_wt.write(i, 1, iID)
            # print "aID:%s iID:%s" % (aID_key_str, iID)
    new_excel_file_data.save("/Users/xiacheng/Desktop/lan_excel_resolved_20180414/doc/new-1.xls")
    print count





def get_key_for_string(dic, str):
    for (key, value) in dic.items():
        strip_value = value.strip()
        strip_str = str.strip()
        if strip_str == strip_value:
            return key

    return False


    # copy_line_to_table(strings_table_date, 0, new_sheet_wt, 0, "aID", "iID")
    # dst_num = 1
    # print "aID num:%d" % len(and_aID_col_data_list)
    # print "total num:%d" % len(strings_aID_col_data_list)
    # for i in xrange(0, len(and_aID_col_data_list)):
    #     key_str_aID = and_aID_col_data_list[i]
    #     # 在mapping表中找到对应的iID及ID
    #     mapping_row_num = get_number_in_col(mapping_table_date, key_str_aID, mapping_aID_col_num)
    #     if not mapping_row_num:
    #         print "==error:mapping:%s \n" % key_str_aID
    #         continue
    #     mapping_iID_str = mapping_table_date.cell(mapping_row_num, mapping_iID_col_num).value
    #     mapping_ID_str = mapping_table_date.cell(mapping_row_num, mapping_ID_col_num).value
    #     # 在string表中找到对应的ID及多语言
    #     strings_row_num = get_number_in_col(strings_table_date, mapping_ID_str, strings_ID_col_num)
    #     if not strings_row_num:
    #         print "==error:strings:%s \n" % key_str_aID
    #         continue
    #     copy_line_to_table(strings_table_date, strings_row_num, new_sheet_wt, dst_num, key_str_aID, mapping_iID_str)
    #     dst_num += 1

    new_excel_file_data.save("/Users/xiacheng/Desktop/lan_excel_resolved_20180414/doc/new-1.xls")






    # for i in xrange(0, len(strings_ID_col_data_list)):
    #     key_str = strings_ID_col_data_list[i]
    #     # 获取mapping表中,此ID在的行数
    #     maping_id_row_num = get_number_in_col(mapping_table_date, key_str, mapping_ID_col_num)
    #     # 如果是第一行或者没有找到,则直接找下一个
    #     if not maping_id_row_num:
    #         continue
    #     # 找到对就的iID和aID
    #     aID_for_key_str = mapping_aID_col_data_list[maping_id_row_num]
    #     iID_for_key_str = mapping_iID_col_data_list[maping_id_row_num]
    #     # 写入到strings表中对应位置
    #     strings_table_date_wt.write(i, strings_aID_col_num, aID_for_key_str)
    #     strings_table_date_wt.write(i, strings_iID_col_num, iID_for_key_str)
    #     print key_str
    #     count = count + 1





def copy_line_to_table(src_table, src_line, dst_table, dst_line, aID, iID):
    # print "srcLine:%d dstLine:%d" % (src_line, dst_line)
    src_line_list = src_table.row_values(src_line)
    dst_table.write(dst_line, 0, aID)
    dst_table.write(dst_line, 1, iID)
    # print src_line_list
    for i in xrange(len(src_line_list)):
        if i < 2:
            continue
        key = src_line_list[i]
        dst_table.write(dst_line, i, key)





# 获取word在table表中row行中的序号,从0开始
def get_number_in_row(table, word, row):
    row_list = table.row_values(row)
    eval_word = word.strip()
    for i in xrange(0, len(row_list)):
        eval_str = row_list[i].strip()
        if eval_word == eval_str:
            return i
    if len(eval_word) == 0:
        return False
    return False


# 获取word在table表中col列中的序号，从0开始
def get_number_in_col(table, word, col):
    col_list = table.col_values(col)
    eval_word = word.strip()
    for i in xrange(0, len(col_list)):
        eval_str = col_list[i].strip()
        if eval_word == eval_str:
            return i
    if len(eval_word) == 0:
        return False
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




def main():
    excel_path = TEST_PATH
    generate_new_excel(excel_path)



if __name__ == '__main__':
    main()
