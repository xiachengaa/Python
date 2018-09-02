#!/bin/sh
# 将此文件里面的命令放到 Build Phases -> Run Script 脚本中
echo "checking..."
python ./script/langue_check_tool.py  $PROJECT_DIR
if [$? -eq 0]
then
    echo "sucess"
else
    echo "denied"
    exit
fi

echo "finish checking"
