# -*- coding: utf-8 -*-
import os
import commands

list = xrange(0,3)
str = ""

from subprocess import Popen, PIPE, STDOUT

p = Popen(['python', 'func.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
output = p.communicate(input='1\n1\n1\n')[0]
print output;
