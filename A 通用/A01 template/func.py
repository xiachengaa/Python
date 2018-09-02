import os

list = xrange(0,3)
str = ""
for i in list:
    x = raw_input("input a str: ")
    print(x)
    if int(x) == 1:
        print("abc:%d" % int(x))
    str = str + x
print("\n\n%s" % str)