# -*- coding:utf-8 -*-

import xlwt
import xlrd
from xlutils.copy import copy
from config import *
import os
import shutil
import time
from resolve_stringfile import *

default_config()


strings_aID_col_num = 0
strings_iID_col_num = 1
strings_ID_col_num = 2

mapping_ID_col_num = 0
mapping_aID_col_num = 1
mapping_iID_col_num = 2


def generate_new_excel(excel_path):
    xlrd.Book.encoding = "utf-8"
    # 打开excel,并将此excel复制,方便后续写入
    excel_file_data = xlrd.open_workbook(excel_path)
    new_excel_file_data = copy(excel_file_data)

    # 两个table的值
    mapping_table_data = excel_file_data.sheet_by_name(MAPPING_TABLE_NAME)
    strings_table_data = excel_file_data.sheet_by_name(STRING_TABLE_NAME)
    aID_table_data = excel_file_data.sheet_by_name("aID")
    strings_table_data_wt = new_excel_file_data.get_sheet(1)
    android_table_data_wt = new_excel_file_data.add_sheet('Android')

    # mapping表中列
    mapping_ID_col_data_list = mapping_table_data.col_values(mapping_ID_col_num)
    mapping_aID_col_data_list = mapping_table_data.col_values(mapping_aID_col_num)
    mapping_iID_col_data_list = mapping_table_data.col_values(mapping_iID_col_num)

    # strings表中列
    strings_ID_col_data_list = strings_table_data.col_values(strings_ID_col_num)
    strings_aID_col_data_list = strings_table_data.col_values(strings_aID_col_num)
    strings_iID_col_data_list = strings_table_data.col_values(strings_iID_col_num)


    #aID 表中的列
    aID_data_list = aID_table_data.col_values(0)

    '''
    由ID在mapping表中找到对应的aID和iID并复制过来
    '''
    # 能在mapping中找到数目
    mapping_id_find_count = 0
    mapping_id_nofind_count = 0
    nofound_str_list = []
    for i in xrange(1, len(strings_ID_col_data_list)):
        key_str = strings_ID_col_data_list[i]
        # 获取mapping表中,此ID在的行数
        maping_id_row_num = get_number_in_col(mapping_table_data, key_str, mapping_ID_col_num)
        # 如果是第一行或者没有找到,则直接找下一个
        if not maping_id_row_num:
            mapping_id_nofind_count+=1
            nofound_str_list.append(key_str)
            continue
        # 找到对就的iID和aID
        aID_for_key_str = mapping_aID_col_data_list[maping_id_row_num]
        iID_for_key_str = mapping_iID_col_data_list[maping_id_row_num]
        # 写入到strings表中对应位置
        strings_table_data_wt.write(i, strings_aID_col_num, aID_for_key_str)
        strings_table_data_wt.write(i, strings_iID_col_num, iID_for_key_str)
        mapping_id_find_count+=1
    print "==共有%d 个id, 在mapping中找到%d, 未找到%d" % (mapping_id_find_count + mapping_id_nofind_count,
                                                mapping_id_find_count, mapping_id_nofind_count)
    print "没有找到的id如下"
    print nofound_str_list
    print "\n\n"




    '''
    生成Android表,包括aID、iID、ID及多语言
    '''

    copy_line_to_table(strings_table_data, 0, android_table_data_wt, 0, "aID", "iID")
    dst_num = 1  # 要复制到的行标
    print "安卓key总数目:%d" % len(aID_data_list)
    for i in xrange(0, len(aID_data_list)):
        key_str_aID = aID_data_list[i]
        # 在mapping表中找到对应的iID及ID
        mapping_row_num = get_number_in_col(mapping_table_data, key_str_aID, mapping_aID_col_num)
        if not mapping_row_num:
            print "==error:mapping:%s \n" % key_str_aID
            continue
        mapping_iID_str = mapping_table_data.cell(mapping_row_num, mapping_iID_col_num).value
        mapping_ID_str = mapping_table_data.cell(mapping_row_num, mapping_ID_col_num).value
        # 在string表中找到对应的ID及多语言
        strings_row_num = get_number_in_col(strings_table_data, mapping_ID_str, strings_ID_col_num)
        if not strings_row_num:
            print "==error:strings:%s \n" % key_str_aID
            continue
        copy_line_to_table(strings_table_data, strings_row_num, android_table_data_wt, dst_num, key_str_aID,
                           mapping_iID_str)
        dst_num += 1

    print "最终找到的数目:%d" % (dst_num - 1)

    new_excel_file_data.save(NEW_EXCEL_PATH)

    '''
    1.判断已有iID与表中是否一致（zh）
    2.表中没有iID的字段,在.strings文件中是否存在
    '''
    # 打开excel,并将此excel复制,方便后续写入
    xlrd.Book.encoding = "utf-8"
    excel_file_data = xlrd.open_workbook(NEW_EXCEL_PATH)
    new_excel_file_data = copy(excel_file_data)

    # 两个table的值
    mapping_table_data = excel_file_data.sheet_by_name(MAPPING_TABLE_NAME)
    strings_table_data = excel_file_data.sheet_by_name(STRING_TABLE_NAME)
    android_table_data = excel_file_data.sheet_by_name("Android")
    android_table_data_wt = new_excel_file_data.get_sheet(3)
    notfound_table_data_wt = new_excel_file_data.add_sheet("notfoundiniOS")

    # mapping表中列
    mapping_ID_col_data_list = mapping_table_data.col_values(mapping_ID_col_num)
    mapping_aID_col_data_list = mapping_table_data.col_values(mapping_aID_col_num)
    mapping_iID_col_data_list = mapping_table_data.col_values(mapping_iID_col_num)

    # strings表中列
    strings_ID_col_data_list = strings_table_data.col_values(strings_ID_col_num)
    strings_aID_col_data_list = strings_table_data.col_values(strings_aID_col_num)
    strings_iID_col_data_list = strings_table_data.col_values(strings_iID_col_num)

    # aID 表中的列
    aID_data_list = aID_table_data.col_values(0)

    # Android表中的列
    android_iID_data_list = android_table_data.col_values(1)


    #从strings文件找value对应的key值
    string_dic = get_key_value_dic_from_string_file(STRING_FILE_PATH)
    notfound_table_data_wt.write(0, 0, "aID")
    notfound_table_data_wt.write(0, 1, "mapping/strings中均找不到")
    notfound_table_data_wt.write(0, 2, "aID")
    notfound_table_data_wt.write(0, 3, "mapping/strings中均有,但iID不对应")
    notfound_table_data_wt.write(0, 4, "表中iID")
    notfound_table_data_wt.write(0, 5, "string中iID")
    notfound_table_data_wt.write(0, 6, "mapping中找到,.strings中找不到")
    notfound_dst_cout = 1
    notfit_dst_count = 1
    count = 1
    for i in xrange(0, len(android_iID_data_list)):
        key_str_iID = android_iID_data_list[i].strip()
        # 判断需要更正的字段
        if len(key_str_iID) == 0 or key_str_iID == "/" or key_str_iID == "\\":
            # 找到简体中文
            zh_key_str = android_table_data.cell(i, 4).value
            aID_key_str = android_table_data.cell(i, 0).value
            # 去string文件中找到对应的值
            iID = get_key_for_string(string_dic, zh_key_str)
            if not iID:
                notfound_table_data_wt.write(notfound_dst_cout, 0, aID_key_str)
                notfound_table_data_wt.write(notfound_dst_cout, 1, zh_key_str)
                print "mapping/strings中均找不到:key:%s aID:%s" % (zh_key_str, aID_key_str)
                notfound_dst_cout += 1
                continue
            android_table_data_wt.write(i, 1, iID)
        else:
            zh_key_str = android_table_data.cell(i, 4).value.strip()
            iID_key_str = android_table_data.cell(i, 1).value.strip()
            aID_key_str = android_table_data.cell(i, 0).value
            iID = get_key_for_string(string_dic, zh_key_str)

            if not iID:
                print "mapping中找到,.strings中找不到:%s" % zh_key_str
                notfound_table_data_wt.write(count, 6, zh_key_str)
                count += 1
                continue
            else:
                if iID == iID_key_str:
                    continue
                else:
                    notfound_table_data_wt.write(notfit_dst_count, 2, aID_key_str)
                    notfound_table_data_wt.write(notfit_dst_count, 3, zh_key_str)
                    notfound_table_data_wt.write(notfit_dst_count, 4, iID_key_str)
                    notfound_table_data_wt.write(notfit_dst_count, 5, iID)
                    notfit_dst_count += 1
                    print "mapping/strings中均有,但iID不对应:key:%s aID:%s" % (zh_key_str, aID_key_str)

    print "1:%d  2:%d 3:%d" % (notfound_dst_cout-1, notfit_dst_count-1, count)
    #new_excel_file_data.save(FINAL_EXCEL_PATH)

def get_key_for_string(dic, str):
    for (key, value) in dic.items():
        strip_value = value.strip()
        strip_str = str.strip()
        if strip_str == strip_value:
            return key
    return False


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
