# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

index = 1
lastNum = 0
_file = open("HZK16.txt")
final=""
for line in _file.readlines():
    line = line.replace('\n', "")
    num = (index - 1)/23
    if( lastNum != num ):
        lastNum = num
        tbl = line.split(',')
        name = tbl[4]
        w = len(name)
        name = name[3:w-2]
        final = final + name
        
    # print line

    index = index + 1

word = open("word.txt", mode="w")
word.write( final )
word.close()
_file.close()