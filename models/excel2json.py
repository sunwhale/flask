# -*- coding: utf-8 -*-

import xlrd
import json
import codecs
from collections import OrderedDict

def excel2json():
    wb = xlrd.open_workbook('info.xlsx')

    convert_list = []
    sh = wb.sheet_by_index(0)
    title = sh.row_values(0)
    for rownum in range(1, sh.nrows):
        rowvalue = sh.row_values(rownum)
        single = OrderedDict()
        for colnum in range(0, len(rowvalue)):
            print(title[colnum], rowvalue[colnum])
            single[title[colnum]] = rowvalue[colnum]
        convert_list.append(single)
        
    j = json.dumps(convert_list)
    print convert_list
    # with codecs.open('file.json',"w","utf-8") as f:
    #     f.write(j)

if __name__ == "__main__":
    excel2json()