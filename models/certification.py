# -*- coding: utf-8 -*-

import qrcode
import os
import numpy as np
from math import isnan
from PIL import Image,ImageFont,ImageDraw

def gen_qrcode(string, path, logo=""):
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库
    :param string: 二维码字符串
    :param path: 生成的二维码保存路径
    :param logo: logo文件路径
    :return:
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=18,
        border=1
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
        
    img.save(path)

def certification(  img_folder='..//static//img',
                    certification_folder='..//static//certification',
                    number='0',
                    qrcode_text='',
                    name=u'产品名称',
                    furniture_filename='',
                    template_filename=''  ):
    img_folder = img_folder
    certification_folder = certification_folder
    number = number
    template_filename = template_filename
    qrcode_logo = os.path.join(img_folder,'logo.jpg')
    furniture_filename = furniture_filename

    # 打开模板文件
    try:
        img = Image.open(template_filename)
    except:
        return '失败.jpg', u'模板文件错误'
    
    # 放置二维码图片
    try:
        isnan(qrcode_text)
    except:
        qrcode_filename = os.path.join(img_folder,'qrcode.png')
        gen_qrcode(qrcode_text,qrcode_filename,qrcode_logo)
        img_qrcode = Image.open(qrcode_filename)
        box_qrcode = (0, 0, img_qrcode.width, img_qrcode.height)
        region_qrcode = img_qrcode.crop(box_qrcode)
        x = 3780
        y = 260
        box_qrcode = (x, y, x+img_qrcode.width, y+img_qrcode.height)
        img.paste(img_qrcode, box_qrcode)

    # 放置家具图片
    try:
        img_furniture = Image.open(furniture_filename)
    except:
        return '失败.jpg', u'家具图片错误'

    if img_furniture.width > 2900 or img_furniture.height > 2100:
        width_ratio = img_furniture.width/2900.0
        height_ratio = img_furniture.height/2100.0
        zoom_ration = max(width_ratio,height_ratio)
        newWidth = int(img_furniture.width/zoom_ration)
        newHeight = int(img_furniture.height/zoom_ration)
    elif img_furniture.width < 2800 or img_furniture.height < 2000:
        width_ratio = img_furniture.width/2800.0
        height_ratio = img_furniture.height/2000.0
        zoom_ration = max(width_ratio,height_ratio)
        newWidth = int(img_furniture.width/zoom_ration)
        newHeight = int(img_furniture.height/zoom_ration)
    else:
        newWidth = img_furniture.width
        newHeight = img_furniture.height
    img_furniture = img_furniture.resize((newWidth,newHeight),Image.ANTIALIAS)
    box_furniture = (0, 0, img_furniture.width, img_furniture.height)
    region_furniture = img_furniture.crop(box_furniture)
    x = 5280
    y = 2420
    box_furniture = (x-img_furniture.width/2, y-img_furniture.height/2, x+img_furniture.width/2+img_furniture.width%2, y+img_furniture.height/2+img_furniture.height%2)
    img.paste(img_furniture, box_furniture)

    draw=ImageDraw.Draw(img)

    font = ImageFont.truetype('simsun.ttc',120)
    text = name
    x = 1520
    y = 1998
    for i in [0,1,2]:
        for j in [0,1,2]:
            draw.text((x+i,y+j),text,(0,0,0),font=font)

    # 生成证书中的横线，其中gbk的编码是是为了区分全角和半角字符的长度，中文长度为2，英文和数字长度为1。
    for i in range(6):
        draw.line(((1420,2118+i),(1420+len(name.encode('gbk'))*60+200,2118+i)),fill=0)

    font=ImageFont.truetype('simsun.ttc',120)
    text = number
    x = 1775
    y = 1695
    for i in [0,1,2]:
        for j in [0,1,2]:
            draw.text((x+i,y+j),text,(0,0,0),font=font)
        
    font=ImageFont.truetype('simsun.ttc',120)
    text = number
    x = 5635
    y = 510
    for i in [0,1,2]:
        for j in [0,1,2]:
            draw.text((x+i,y+j),text,(0,0,0),font=font)

    filename = 'certification_' + number + '.jpg'
    img.save(os.path.join(certification_folder, filename))

    # img.show()

    return filename, u'完成'

if __name__ == "__main__":
    filename, status = certification(  img_folder='F:\\GitHub\\flask\\static\\img\\',
                    certification_folder='F:\\GitHub\\flask\\static\\certification\\',
                    number='0',
                    qrcode_text=np.nan,
                    name=u'产品名称',
                    furniture_filename='F:\\GitHub\\flask\\static\\uploads\\furniture\\book.jpg',
                    template_filename='F:\\GitHub\\flask\\static\\uploads\\template\\2019.jpg'  )
    print filename, status