#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Author  :   WilliamKyle(WilliamKyle@126.com)
    Date    :   2015/03/12 11:12:33
    Desc    :   Dump binary file
"""


import argparse
import binascii


need_print_address = True
need_print_dump = True
need_print_header = True
dump_to_html = False
line_to_dump = -1

def print_field(content):
    if dump_to_html:
        print '<td>%s</td>' % content,
    else:
        print content,


def print_address(value):
    if not need_print_address :
        return
    content =  '{0: ^8s}'.format(value)
    print_field(content)

def print_dump(value):
    if not need_print_dump :
        return

    content = '{0:_^32s}'.format(value)
    if dump_to_html:
        print '<td colspan=16>%s</td>' % content,
    else:
        print content,

def print_header():
    if not need_print_header :
        return

    if dump_to_html:
        print '<tr>'

    print_address('Address')

    for i in range(16):
        content = '{0: >2X}'.format(i)
        print_field(content)

    print_dump('Dump')

    if dump_to_html:
        print '\n</tr>'
    else:
        print ""

def make_data(file_path):
    try:
        f = file(file_path, "r")
    except Exception as err:
        print err
        exit(-1)

    if dump_to_html:
        print '<table>'

    print_header()
    line = f.read(16)
    line_no = 0
    while line:
        if line_no / 16 == line_to_dump:
            break;

        if dump_to_html:
            print '<tr>'

        # Address
        if need_print_address :
            content = '{0:0>8X}'.format(line_no)
            print_field(content)

        # Data
        for c in line:
            content = binascii.b2a_hex(c)
            print_field(content)
        if len(line) < 16:
            for s in range(16-len(line)):
                print_field('  ')

        # Dump
        if need_print_dump :
            for c in line:
                n = ord(c)
                if n < 127 and n > 31:
                    print_field(chr(n))
                else:
                    print_field('.')

        if dump_to_html:
            print '\n</tr>'
        else:
            print ""

        line = f.read(16)
        line_no += 16

    if dump_to_html:
        print '</table>'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nh", help="Do NOT dispaly header line", action="store_true")
    parser.add_argument("--na", help="Do NOT dispaly Address field", action="store_true")
    parser.add_argument("--nd", help="Do NOT dispaly Dump field", action="store_true")
    parser.add_argument("--html", help="Dump into html table", action="store_true")
    parser.add_argument("-l", "--line", type=int, help="How many lines to dump")
    parser.add_argument("file", help="The file need to dump")
    args = parser.parse_args()
    
    if args.nh:
        need_print_header = False
    if args.na:
        need_print_address = False
    if args.nd:
        need_print_dump = False
    if args.html:
        dump_to_html = True
    if args.line:
        line_to_dump = args.line

    make_data(args.file)
