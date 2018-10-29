import numpy as np
import glob
import argparse
import imutils
import cv2
import math
import os, sys
import xml.etree.ElementTree as ET
from PIL import Image

"""
	xml is created by LabelImg v1.2.2 application
"""

# def FlipIMG(xml_file,new_xml_file,img_file,new_img_file,FileName,Type):	
# 		print(xml_file)
# 		# Reading annotation infor	 
# 		tree = ET.parse(xml_file)
# 		root = tree.getroot()
# 		n=0;  
# 		file_name = root.find('filename')
# 		path = root.find('path')
# 		file_name.text = FileName
# 		path.text = img_file

# 		### load the image from disk
# 		image = cv2.imread(img_file)
# 		# image_clone = image.copy()
# 		final_img = cv2.flip( image, Type )

# 		Height = int(final_img.shape[0])
# 		Width = int(final_img.shape[1])
		
# 		for sz in root.findall('size'):
# 			w = sz.find('width')
# 			h = sz.find('height')

# 			w.text = str(Width)
# 			h.text = str(Height)

# 		for obj in root.findall('object'):			
# 			bndbox= obj.find('bndbox')	
# 			xmin = bndbox.find('xmin')
# 			ymin = bndbox.find('ymin')
# 			xmax = bndbox.find('xmax')
# 			ymax = bndbox.find('ymax')
		
# 			### Fliping images
# 			if Type==0 :
# 				x_min_new = int(xmin.text)
# 				y_min_new = Height - int(ymax.text)
# 				x_max_new = int(xmax.text)
# 				y_max_new = Height - int(ymin.text)
# 			if Type==1 :
# 				x_min_new = Width - int(xmax.text)
# 				y_min_new = int(ymin.text)
# 				x_max_new = Width - int(xmin.text)
# 				y_max_new = int(ymax.text)

# 			xmin.text = str(x_min_new)
# 			ymin.text = str(y_min_new)
# 			xmax.text = str(x_max_new)
# 			ymax.text = str(y_max_new)

# 			print(xmin.text)
# 			cv2.imwrite(new_img_file, final_img)

# 		tree.write(new_xml_file)

def RotateIMG(xml_file,new_xml_file,img_file,new_img_file,FileName,rotate_angle):	
		print(xml_file)
		# Reading annotation infor	 
		tree = ET.parse(xml_file)
		root = tree.getroot()
		n=0;  
		file_name = root.find('filename')
		path = root.find('path')
		file_name.text = FileName
		path.text = img_file


		### load the image from disk
		image = cv2.imread(img_file)
		# image_clone = image.copy()
		final_img = imutils.rotate_bound(image, rotate_angle)

		Height = int(final_img.shape[0])
		Width = int(final_img.shape[1])
		
		for sz in root.findall('size'):
			w = sz.find('width')
			h = sz.find('height')

			w.text = str(Width)
			h.text = str(Height)

		for obj in root.findall('object'):			
			bndbox= obj.find('bndbox')	
			xmin = bndbox.find('xmin')
			ymin = bndbox.find('ymin')
			xmax = bndbox.find('xmax')
			ymax = bndbox.find('ymax')
	
			# # Highlighting hand region 
			Rect = cv2.rectangle(image,(int(xmin.text), int(ymin.text)),(int(xmax.text), int(ymax.text)),(255,255,255), cv2.FILLED)

			# Rotating images
			rotated = imutils.rotate_bound(image, rotate_angle)

			# Convert to gray scale
			gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
			# Theshold to get the hand box region
			ret,gray = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
			# Finding contours
			_,contours,_ = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

			cnt = max(contours, key=cv2.contourArea)
			# cnt = contours[0]

			# Creating rotated rectangle
			rect = cv2.minAreaRect(cnt)

			# Getting minAreaRect info
			c_point_x=int(rect[0][0])
			c_point_y=int(rect[0][1])
			width=int(rect[1][0])
			height=int(rect[1][1])
			angle=int(rect[2])

			x_min_new = c_point_x-width/2 
			y_min_new = c_point_y-height/2 
			x_max_new = c_point_x+width/2 
			y_max_new = c_point_y+height/2

			xmin.text = str(x_min_new)
			ymin.text = str(y_min_new)
			xmax.text = str(x_max_new)
			ymax.text = str(y_max_new)

			print(xmin.text)
			cv2.imwrite(new_img_file, final_img)

		tree.write(new_xml_file)	
		
if __name__ == '__main__':    
	anno_dir="/home/real-vigga/kinect_dataset/xml_new/"
	imgs_dir="/home/real-vigga/kinect_dataset/image/"
	new_anno_dir="/home/real-vigga/kinect_dataset/rotated_xml/"
	new_img_dir="/home/real-vigga/kinect_dataset/rotated/"
	rotate_angle = -10
	flip_type = 1

	anno_paths=glob.iglob(os.path.join(anno_dir, "*.xml"))
	anno_paths=list(anno_paths)
	img_paths = glob.iglob(imgs_dir + '*.*')
	img_paths = list(img_paths)

	np=len(anno_paths)
	print("Number of samples: ",np)
	i=0;	
	n=0;

	while i <np:		
		anno_path=anno_paths[i]	
		if not os.path.isfile(anno_path):
			i=i+1
			continue		  
		print (anno_path)
		anno, ext = os.path.splitext(os.path.basename(anno_path))			
		print ('Processing {:d}/{:d} {:s}...'.format(i,np,anno))
		img_path = imgs_dir + anno + '.png'
		if not os.path.isfile(img_path):
			img_path = imgs_dir + anno + '.jpg'
		file_name = anno + '_' + str(rotate_angle) + 'd' + '.png'
		new_xml_path = new_anno_dir + anno + '_' + str(rotate_angle) + 'd' + '.xml'
		new_img_path = new_img_dir + file_name
		
		RotateIMG(anno_path, new_xml_path, img_path, new_img_path, file_name, rotate_angle) 
		# FlipIMG(anno_path, new_xml_path, img_path, new_img_path, file_name, flip_type)

		percent = int(i/(np * 0.01))
		print('Counting {:d} %   |   {:d}'.format(percent,i))

		i=i+1
