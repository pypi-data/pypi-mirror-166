#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 15:09
# @Author  : jeremy
# @File    : TEST.py


def invert_8(x):
    y=0

    for i in range(8):

        if(0!=(x&(1<<i))):
            # print(i)
            # print(1<<(7-i))
            y|=1<<(7-i)
    return y
def crc166(x):
    y = 0

    for i in range(16):

        if (0 != (x & (1 << i))):
            # print(i)
            # print(1<<(7-i))
            y |= 1 << (15 - i)
    return y

def crc16(p,len):
    wCRCin = 0x0
    wCPoly = 0x1021
    wChar = 0
    for i in range(len):
        pidx = (i & 0xFFFFFFFC) | (3 - (i & 3))
        wChar = invert_8(p[pidx])
        wCRCin ^= (wChar << 8)

        for j in range(8):
            if (0x8000 == (wCRCin & 0x8000)):
                wCRCin = (wCRCin << 1) ^ wCPoly
            else:
                wCRCin <<= 1
    return crc166(wCRCin)
def checksum(p,len,offset=0):
    sum=0
    i=offset
    for i in range(len):
        sum+=p[i]
    return sum&0xFF
    pass
def version_check():
    pass
    print(checksum([0xFA, 0x01, 0x02, 0x00, 0x09, 0x00, 0x6, 0x1A, 0x80], 9))
    #FA 01 02 00 09 00 06 1A 80 A6 7E


# print(checksum([0xFA,0x01,0x02,0x00,0x09,0x00,0x6,0x1A,0x80],9))

# print(crc16([0xFA,0x01,0x02,0x00,0x09,0x00,0x6,0x1A,0x80],9))
#
# input_s ="01 02 03 04 05 06 07 08 99 1A 0B"
# input_s = input_s.strip()
# send_list = []
# while input_s != '':
#     try:
#         num = int(input_s[0:2], 16)
#     except ValueError:
#         print(0)
#     input_s = input_s[2:].strip()
#     send_list.append(num)
# input_s = bytes(send_list)
# print(send_list)
# print(input_s)
# rev = to_hexstring(send_list)
# print(rev)

#b'\xe6\x88\x91\xe6\x98\xaf\xe4\xb8\x9c\xe5\xb0\x8f\xe4\xb8\x9c'
#b'\xce\xd2\xca\xc7\xb6\xab\xd0\xa1\xb6\xab'
# if(0xFA==250):
#     print(123)
# data=[5,6]
# print('APP校验码错误，程序烧录失败，校验码为：0x{:02X}{:02X}'.format(data[0],data[1]))
text='23'
print("%05d:" % 1+text)