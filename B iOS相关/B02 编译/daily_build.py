# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
import re
import shutil

# ---------------需要修改----------------
# 项目根目录 能够找到对应的WORKSPACE文件
g_work_dir = "/Users/xiacheng/Desktop/Auto/Compile"

g_svn_path = "https://x03556@61.164.52.185/svn/APP/branches_project/EZView_SimpleApp_iOS"

g_code_dir_name = "EZView_SimpleApp_iOS/ios"

g_build_configuation = "Release"

g_project_path = os.path.join(g_work_dir, g_code_dir_name)

# 打包后ipa临时存储目录
g_target_IPA_path = "%s/IPA" % (g_project_path)

g_app_path = "%s/build/Build/Products/%s-iphoneos/EZView.app" \
           % (g_project_path, g_build_configuation)

g_build_path = os.path.join(g_project_path, "build")

g_export_plist_path = "/Users/xiacheng/Desktop/Auto/Compile/EZView_SimpleApp_iOS/ios/ExportOptions.plist"

g_archive_path = os.path.join(g_build_path, "archive/EZViewer.xcarchive")

# ---------------需要修改----------------

# 拉取代码
# def clean_and_get_code(work_dir, svn_path):
#     if not os.path.exists(work_dir):
#         os.mkdir(work_dir)
#     else:
#         shutil.rmtree(work_dir)
#         os.mkdir(work_dir)
#     get_code_cmd = "cd %s;svn co %s" % (work_dir, svn_path)
#     os.system(get_code_cmd)


# 指定项目下编译目录
def build_project():

    #update
    update_cmd = "cd %s;cd ..;svn up ." % g_project_path
    os.system(update_cmd)
    createDir(g_build_path)
    os.system('cd %s;xcodebuild -list' % g_project_path)
    os.system(
        'cd %s;xcodebuild archive -workspace EZViewer.xcworkspace  -scheme EZViewer -configuration %s  -archivePath '
        '%s' % (g_project_path, g_build_configuation, g_archive_path))
    if not os.path.exists(g_app_path):
        throw_error('编译失败，请查看工程配置是否正确或其他错误')


# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在指定位置
def build_ipa():
    print("build ipa start")
    createDir(g_target_IPA_path)
    export_cmd = "xcodebuild -exportArchive -exportOptionsPlist %s -archivePath  " \
                 "%s -exportPath %s -configuration %s" % (g_export_plist_path, g_archive_path,
                                                          g_target_IPA_path, g_build_configuation)
    #os.system('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s' % (g_app_path, g_target_IPA_path, ipa_filename))
    os.system(export_cmd)
    ori_ipa_path = os.path.join(g_target_IPA_path, "EZViewer.ipa")
    global ipa_filename
    ipa_filename = time.strftime('EZViewer_%Y-%m-%d-%H-%M-%S.ipa', time.localtime(time.time()))
    ipa_path = '%s/%s' % (g_target_IPA_path, ipa_filename)
    shutil.move(ori_ipa_path, ipa_path)
    print ipa_path
    if not os.path.exists(ipa_path):
        throw_error('打包失败，请重试')


def publish_ipa():
    print "publish_ipa"
    ipa_path = '%s/%s' % (g_target_IPA_path, ipa_filename)
    publish_cmd = "fir publish %s -Q -s ly1" % ipa_path
    os.system(publish_cmd)

# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd %s;xcodebuild clean' % g_project_path)  # clean 项目


def createDir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print '%s 文件目录创建成功' % path
    else:
        print '%s 目录已存在' % path


def throw_error(message):
    raise Exception(message)


def main():
    # 清理项目
    #clean_project_mkdir_build()
    # 编译项目
    build_project()
    # 打包ipa
    build_ipa()
    # 上传fir
    publish_ipa()
    print 'complete all'


if __name__ == '__main__':
    main()
