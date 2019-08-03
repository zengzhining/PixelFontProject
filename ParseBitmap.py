# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import binascii
import os
import time
import threading
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

def resizePicture( fileName ):
    im = Image.open(fileName)
    out = im.resize(( 128 , 128))
    out.save( fileName , 'png' )



def drawPicture( font_tbl, fileName ):
    w = 16
    h = 16
    image = Image.new('RGB',( w,h ), (255,255,255))
    draw = ImageDraw.Draw( image )
    for y in range(h):
        # print(y)
        row = font_tbl[y]
        for x in range(w):
            # print(str(x) + " " + str(y) )
            if( row[x] ):
                draw.point((x,y), fill=(0,0,0))
    image.save(fileName, 'png')


def getFontList( _name ):
    # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示，需要32个字节才能显示一个汉字
    # 之所以32字节：256个点每个点是0或1，那么总共就是2的256次方，一个字节是2的8次方
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16) 

    #获取中文的gb2312编码，一个汉字是由2个字节编码组成
    gb2312 = text.encode('gb2312')
    #将二进制编码数据转化为十六进制数据
    hex_str = binascii.b2a_hex(gb2312)
    #将数据按unicode转化为字符串
    # result = str(hex_str, encoding='utf-8')
    result = str(hex_str)

    #前两位对应汉字的第一个字节：区码，每一区记录94个字符
    area = eval('0x' + result[:2]) - 0xA0

    #后两位对应汉字的第二个字节：位码，是汉字在其区的位置
    index = eval('0x' + result[2:]) - 0xA0

    #汉字在HZK16中的绝对偏移位置，最后乘32是因为字库中的每个汉字字模都需要32字节
    offset = (94 * (area-1) + (index-1)) * 32

    font_rect = None

    #读取HZK16汉字库文件
    with open("HZK16", "rb") as f:
        #找到目标汉字的偏移位置
        f.seek(offset)
        #从该字模数据中读取32字节数据
        font_rect = f.read(32)

    #font_rect的长度是32，此处相当于for k in range(16)
    for k in range(len(font_rect) // 2):
        #每行数据
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                #此处&为Python中的按位与运算符
                
                flag = ((ord)(asc)) & KEYS[i]
                # flag = False
                #数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                row_list.append(flag)
    return rect_list

def getChinese( content, index ):
    return content[index * 3 : index * 3 +3]


# print '参数个数为:', len(sys.argv), '个参数。'
# print '参数列表:', str(sys.argv)
# print sys.argv[1]
# _file = open("word.txt", mode='r')
# _content = _file.read()
# print _content
# index = 1
# num = len(_content)/3

# _log = open("config.txt", mode='w')

# for i in range( num ):
#     text = getChinese( _content, i )
#     print "start to process %s" % ( text )
#     # text = sys.argv[1]
#     name = "%d.png" % ( i )
#     svgName = "%d.svg" % (i)
#     _list = getFontList( text )
#     drawPicture( _list, name )
#     resizePicture( name )
#     print "start to change to svg"
#     command = "./png2svg.sh %s" % ( name )
#     print command
#     os.system( command )
#     # write to data
#     line = "%s,%s\n" % ( text, svgName )
#     _log.write( line )
# _log.close()
# _file.close()

# Parse pe file
def changePeFile( fontName, fileName ) :
    print "changePeFile:%s %s" % ( fontName, fileName )
    peFile = open( "convert.pe", mode='r+' )
    firstLine=peFile.readline()
    nameLine = peFile.readline()
    fileLine = peFile.readline()
    last = peFile.read()
    peFile.close()
    nameLine = "fontName = \"%s\" \n" % ( fontName )
    fileLine = "svg_file = \"%s\" \n" % ( fileName )
    # print firstLine
    # print nameLine
    # print fileLine
    # print last
    final = firstLine + nameLine + fileLine + last
    peFile = open( "convert.pe", mode='w' )
    peFile.write(final)
    peFile.close()
    output = os.system( "FontForge -script convert.pe test.sfd" )

## read config.txt
_config = open("config.txt", mode='r')
fromLine = 781
toLine = 810
lineNum = 1
for line in _config.readlines():
    if( lineNum >= fromLine and lineNum <= toLine ):
        line = line.replace('\n',"")
        tbl = line.split(',')
        changePeFile( tbl[0], tbl[1] )
        time.sleep(0.5)
        print line
    
    lineNum = lineNum+1
    



#changePeFile( "好", "0.svg" )
#output = os.popen( "FontForge -script convert.pe test.sfd" )

