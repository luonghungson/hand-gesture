import numpy as np
import glob
import os, sys
import xml.etree.ElementTree as ET
from PIL import Image

"""
	xml is created by LabelImg v1.2.2 application
"""
def AnnotationConvertXML2TXT(im_size,xmlfile,txtfile):	
	with open(txtfile, "w") as text_file:	
		print(xmlfile)
		print(txtfile) 
		# Reading annotation infor	 
		tree = ET.parse(xmlfile)
		root = tree.getroot()  
		for obj in root.findall('object'):			
			id = int(obj.find('name').text)
			#print name
			bndbox= obj.find('bndbox')			
			xmin = int(bndbox.find('xmin').text)
			ymin = int(bndbox.find('ymin').text)
			xmax = int(bndbox.find('xmax').text)
			ymax = int(bndbox.find('ymax').text)

			dw=1.0/im_size[0]
			dh=1.0/im_size[1]			
			x=(xmin+xmax)/2.0
			y=(ymin+ymax)/2.0
			w=xmax-xmin
			h=ymax-ymin

			x=x*dw
			w=w*dw
			y=y*dh
			h=h*dh
			# if id==0 or id==3:
			# 	id=7
			# elif id==1:
			# 	id=5
			# elif id==2:
			# 	id=6
			# elif id==4:
			# 	id=0
			text_file.write("%d %f %f %f %f\n" % (id,x,y,w,h))		

if __name__ == '__main__':    
	anno_dir="/home/real-vigga/kinect_dataset/rotated_xml"
	imgs_dir="/home/real-vigga/kinect_dataset/rotated/"
	txt_anno_dir="/home/real-vigga/kinect_dataset/rotated_labels/"
	anno_paths=glob.iglob(os.path.join(anno_dir, "*.xml"))
	anno_paths=list(anno_paths)

	img_paths = glob.iglob(imgs_dir + '*.*')
	img_paths = list(img_paths)

	np=len(anno_paths)
	print("Number of samples: ",np)
	i=0;	
	while i <np:		
		anno_path=anno_paths[i]	
		img_path = img_paths[i]
		if not os.path.isfile(anno_path):
			i=i+1
			continue		  
		print (anno_path)
		anno, ext = os.path.splitext(os.path.basename(anno_path))			
		print ('Processing {:d}/{:d} {:s}...'.format(i,np,anno))		
		# img_path=imgs_dir+ anno +'.png'   
		img=Image.open(img_path)
		w=int(img.size[0])
		h=int(img.size[1])	
		print("{:d}, {:d}".format(w,h))	
		txt_file=txt_anno_dir+ anno +'.txt'
		AnnotationConvertXML2TXT((w,h),anno_path,txt_file)  
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
			
