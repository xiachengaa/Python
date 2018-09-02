# -*-coding:utf-8-*-
import os
import codecs
import chardet

# 忽略文件夹、文件列表(文件、路径中饮食此列表中的字符将会被忽略，不区分大小写)
ignore_file_list = ["thirdlibrary", ".a", ".png"]
#统计区间,如："16160:16207"
# revision_interval = "16160:16207"


# 1. 生成diff文件,直接在运行文件夹生成
def create_diff_file(project_path, revision_interval_str):
    file_path = os.path.join(project_path, "svn_diff.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
    diff_cmd = "cd %s;svn diff -r %s > svn_diff.txt" % (project_path, revision_interval_str)
    os.system(diff_cmd)


# 2. 对diff文件进行处理：1) 过滤掉某些文件夹里面的内容
def resolve_diff_file(project_path):
    file_path = os.path.join(project_path, "svn_diff.txt")
    file_handle = codecs.open(file_path, 'r', get_file_encode_format(file_path))
    dict = {}
    for line in file_handle:
        if line.startswith("Index:"):
            key = line.split(':')[-1].strip()
            if key not in dict:
                dict[key] = [0, 0]
        if line.startswith('+') and len(line.strip()) > 1:
            dict[key][0] += 1
        if line.startswith('+++'):
            dict[key][0] -= 1
        if line.startswith('-') and len(line.strip()) > 1:
            dict[key][1] += 1
        if line.startswith('---'):
            dict[key][1] -= 1

    ExcludeFileNum = 0
    AddLineNum = 0
    DelLineNum = 0
    TotalLineNum = 0
    TotalFileNum = len(dict.keys())
    for file in dict.keys():
        if file == '.':
            TotalFileNum -= 1
        elif need_ignore_file(file):
            print "Skipping file : %s", file
            ExcludeFileNum += 1
        else:
            AddLineNum += dict[file][0]
            DelLineNum += dict[file][1]
    TotalLineNum = AddLineNum + DelLineNum

    print "===============代码行差异为：=================\n"
    print "新增的代码行 = ", AddLineNum, " 行"
    print "删除的代码行 = ", DelLineNum, " 行\n"
    print "代码行变更总计 = ", TotalLineNum, " 行\n"
    print "变更文件总数 = ", TotalFileNum, " 个\n"
    print "排除文件总数 = ", ExcludeFileNum, " 个\n"
    print "计入文件总数 = ", TotalFileNum - ExcludeFileNum, " 个\n"
    print "=============代码行统计完成！================="


def need_ignore_file(file_name):
    # 1.过滤掉的文件夹，未考虑文件夹重名（在不同层次）
    for key_word in ignore_file_list:
        if contains_str(file_name, key_word):
            return True
    return False


# 获取文件编码格式
def get_file_encode_format(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    # TD 有精确度参数，后面可以判断一下，这里不影响
    format_str = chardet.detect(data)['encoding']
    f.close()
    return format_str


def contains_str(ori_str, str):
    ori_str_low = ori_str.lower()
    str_low = str.lower()
    if str_low in ori_str_low:
        return True
    else:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def main():
    project_path = raw_input('请输入工程文件路径：')
    project_path = project_path.strip()
    start_revision = raw_input('请输入开始版本号(统计时不包括此次提交):')
    start_revision = start_revision.strip()
    end_revision = raw_input('请输入终止版本号(统计时包括此次提交):')
    end_revision = end_revision.strip()
    if (not is_number(start_revision)) or (not is_number(end_revision)):
        print "输入版本号非数字"
        exit(1)
    revision_str = "%s:%s" % (start_revision, end_revision)
    create_diff_file(project_path, revision_str)
    resolve_diff_file(project_path)


if __name__ == "__main__":
    main()
