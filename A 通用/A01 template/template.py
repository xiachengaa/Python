# -*- coding: utf-8 -*-

###############1、时间字符串获取################
#
#%y 两位数的年份表示（00-99）
#%Y 四位数的年份表示（000-9999）
#%m 月份（01-12）
#%d 月内中的一天（0-31）
#%H 24小时制小时数（0-23）
#%I 12小时制小时数（01-12） 
#%M 分钟数（00=59）
#%S 秒（00-59）

#%a 本地简化星期名称
#%A 本地完整星期名称
#%b 本地简化的月份名称
#%B 本地完整的月份名称
#%c 本地相应的日期表示和时间表示
#%j 年内的一天（001-366）
#%p 本地A.M.或P.M.的等价符
#%U 一年中的星期数（00-53）星期天为星期的开始
#%w 星期（0-6），星期天为星期的开始
#%W 一年中的星期数（00-53）星期一为星期的开始
#%x 本地相应的日期表示
#%X 本地相应的时间表示
#%Z 当前时区的名称
#%% %号本身 
import time
time_str = time.strftime("'%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
###############时间字符串获取################


###############2、遍历文件夹################
# root，当前所在的目录，dirs，当前目录下的文件夹, files，当前目录下的文件
for root, dirs ,files in os.walk("test_three_image"): 
    for file in files:
        new_file_name = "%03d_%s.JPG" % (i, time_str)
        os.rename(os.path.join(root, file), os.path.join(root, new_file_name)) 
        print "oldName:%s newName:%s\n" % (file, new_file_name)
###############遍历文件夹################
		
###############3、获取输入################	
# 从命令行读取一行
str = raw_input("enter a word:")
# 输入密码
import getpass
password=getpass.getpass('请输入密码：')
###############3、获取输入################

###############4、在shell中执行及交互################
# 后续如果需要更复杂的操作要学习一下subprocess
# 只返回执行结果（是否报错，0或1）
import os
os.system(cmd)
# 获取返回结果及输出 
import commands
(status, output) = commands.getstatusoutput(cmd)
# 从命令行获取参数再执行(如python test.py abc bcd)
if(len(sys.argv) < 3)
    print("please input tow arguments!")
	sys.exit(1)
arg0 = sys.argv[1] #arg0 is .py
# 与shell交互3次，每次需要输入时均输入1
p = Popen(['python', 'func.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
output = p.communicate(input='1\n1\n1\n')[0]
###############4、在shell中执行及交互################


###############5、文件操作################
# 删除、新建文件夹、检查是否存在
import shutil
shutil.rmtree(dirname)

if not os.path.exists(dir_name):
    os.mkdir(dirname)
# 移动、复制、重命名
shutil.move(srcfile, dstfile)
shutil.copyfile(srcfile, dstfile)
os.rename(ori_name, target_name)

# 文件名操作：后缀获取、拼接
# 判断是否是绝对路径：
os.path.isabs()
os.path.abcpath() # 获取绝对路径

# 返回一个路径的目录名和文件名:
os.path.split() eg os.path.split(‘/home/swaroop/byte/code/poem.txt’) 结果：(‘/home/swaroop/byte/code’, ‘poem.txt’)

# 分离扩展名：
str = os.path.splitext()[1]

# 获取路径名：
os.path.dirname()

# 获取文件名：
os.path.basename() 

# 文件名拼接
os.path.join("路径", "文件名.txt")
###############5、文件操作################


###############6、字符串操作################
# 替换
new_str = str.replace(old, new, [max]) # max 为可选参数，最多替换多少次

# 是否包含判断，不区分大小写
def contain_str(full_str, search_str):
    full_str_lower = full_str.lower()
	search_str_lower = search_str.lower()
	if search_str_lower in full_str_lower:
        return True
    else:
        return False	
###############6、字符串操作################

###############7、环境变量操作################
# 得到当前工作目录，即当前Python脚本工作的目录路径: 
os.getcwd()
# 读取和设置环境变量:
os.getenv() 与 os.putenv()
# 给出当前平台使用的行终止符:
os.linesep #Windows使用’\r\n’，Linux使用’\n’而Mac使用’\r’
# 指示你正在使用的平台：
os.name  #对于Windows，它是’nt’，而对于Linux/Unix用户，它是’posix’
#  判断当前是python2还是python3
###############7、环境变量操作################

if __name__ == '__main__':
    main()

		
		
