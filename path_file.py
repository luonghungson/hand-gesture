import numpy as np
import glob
import os, sys
import xml.etree.ElementTree as ET
from PIL import Image

"""
	xml is created by LabelImg v1.2.2 application
"""

text_file=open('/home/real-vigga/kinect_dataset/train_new.txt', 'w')
	

if __name__ == '__main__':    
	imgs_dir="/home/real-vigga/kinect_dataset/image/"

	# anno_paths=glob.iglob(os.path.join(anno_dir, "*.xml"))
	# anno_paths=list(anno_paths)

	img_paths = glob.iglob(imgs_dir + '*.*')
	img_paths = list(img_paths)

	np=len(img_paths)
	print("Number of samples: ",np)
	i=0;	
	while i <np:		
		img_path = img_paths[i]
		if not os.path.isfile(img_path):
			i=i+1
			continue		  
		print (img_path)
		# anno, ext = os.path.splitext(os.path.basename(anno_path))			
		# print ('Processing {:d}/{:d} {:s}...'.format(i,np,anno))
		
		# img_path = imgs_dir+ anno + ".png"

		text_file.write("%s\n" % (img_path))
		i=i+1 


	# for root, dirs, files in os.walk(anno_dir):
	# 	for xml_name in files:    
	# 		print ("Processing {:s}...".format(xml_name))  
	# 		xml_file=os.path.join(root, xml_name) 
	# 		file_name=os.path.splitext(xml_name)[0]			
	# 		txt_file=txt_anno_dir+ file_name +'.txt' 
	# 		img_file=imgs_dir+ file_name +'.png'
	# 		img=Image.open(img_file)
	# 		w=int(img.size[0])
	# 		h=int(img.size[1])			
	# 		AnnotationConvertXML2TXT((w,h),xml_file,txt_file)          
			
