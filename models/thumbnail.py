# -*- coding: utf-8 -*-

import os
from PIL import Image

def thumbnail(filename,original_folder,thumbnail_folder):
	original_fullname = os.path.join(original_folder,filename)
	img = Image.open(original_fullname)
	if img.width > 128 or img.height > 128:
		width_ratio = img.width/128.0
		height_ratio = img.height/128.0
		zoom_ration = max(width_ratio,height_ratio)
		newWidth = int(img.width/zoom_ration)
		newHeight = int(img.height/zoom_ration)
		img.thumbnail((newWidth,newHeight),Image.ANTIALIAS)

	thumbnail_fullname = os.path.join(thumbnail_folder,filename)
	img.save(thumbnail_fullname,"JPEG")

if __name__ == "__main__":
	original_folder = 'F:\\GitHub\\flask\\static\\uploads\\furniture'
	thumbnail_folder = 'F:\\GitHub\\flask\\static\\uploads\\furniture_thumbnail'
	filename_list = os.listdir(original_folder)
	for filename in filename_list:
		thumbnail(filename,original_folder,thumbnail_folder)