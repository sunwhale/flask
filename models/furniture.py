# -*- coding: utf-8 -*-

import time
import datetime
import os

def TimeStampToTime(timestamp):
	"""把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12"""
	timeStruct = time.localtime(timestamp)
	# return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
	return time.strftime('%Y-%m-%d',timeStruct)

def get_FileSize(filePath):
	"""获取文件的大小,结果保留两位小数，单位为MB"""
	fsize = os.path.getsize(filePath)
	fsize = fsize/float(1024*1024)
	return round(fsize,2)

def get_FileAccessTime(filePath):
	"""获取文件的访问时间"""
	t = os.path.getatime(filePath)
	return TimeStampToTime(t)

def get_FileCreateTime(filePath):
	"""获取文件的创建时间"""
	t = os.path.getctime(filePath)
	return TimeStampToTime(t)

def get_FileModifyTime(filePath):
	"""获取文件的修改时间"""
	t = os.path.getmtime(filePath)
	return TimeStampToTime(t)

if __name__ == "__main__":
	original_folder = 'F:\\GitHub\\flask\\static\\uploads\\furniture'
	thumbnail_folder = 'F:\\GitHub\\flask\\static\\uploads\\furniture_thumbnail'
	filename_list = os.listdir(original_folder)
	for filename in filename_list:
		print filename
		print get_FileSize(os.path.join(original_folder,filename)), get_FileAccessTime(os.path.join(original_folder,filename)), get_FileCreateTime(os.path.join(original_folder,filename)), get_FileModifyTime(os.path.join(original_folder,filename))