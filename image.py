import cv2
import numpy as np


img = cv2.resize(cv2.imread('2.jpg'), (800, 600))  



sec = 5
frames_per_sec = 120
frames = sec*frames_per_sec


orig_x = 400
orig_y = 300


dest_x = 800
dest_y = 300


delta_x = dest_x - orig_x
delta_y = dest_y - orig_y

rate_x = delta_x*1.0/frames
rate_y = delta_y*1.0/frames

orig_zoom = 1
dest_zoom = 3

#how to deal with zooming from larger to smaller
delta_zoom = (dest_zoom-orig_zoom)
rate_zoom = delta_zoom*1.0/frames

window_width = 800
window_height = 600


for x in range(0,int(frames)):

	img_height , img_width , chan = img.shape


	point_x = orig_x+rate_x*x
	point_y = orig_y+rate_y*x

	#scaled_img_width  = int(img_width+img_width*rate_zoom*x)
	#scaled_img_height = int(img_height+img_height*rate_zoom*x)

	temp = 1+1*rate_zoom*x
	resized_image = cv2.resize(img, None,fx=temp,fy=temp)

	scaled_img_height , scaled_img_width , chan = resized_image.shape
	new_point_x = point_x*scaled_img_width/img_width
	new_point_y = point_y*scaled_img_height/img_height


	larger_width = scaled_img_width*2+100
	larger_height = scaled_img_height*2+100

	blank_image = np.zeros((larger_height,larger_width,3), np.uint8)	
	#print "Blank",blank_image.shape

	new_img_height , new_img_width , chan = resized_image.shape
	#print "Resized",resized_image.shape
	calc_height = (larger_height/2+scaled_img_height/2)-(larger_height/2-scaled_img_height/2)
	calc_width = (larger_width/2+scaled_img_width/2) - (larger_width/2-scaled_img_width/2)


	blank_image[larger_height/2-scaled_img_height/2:larger_height/2+scaled_img_height/2,larger_width/2-scaled_img_width/2:larger_width/2+scaled_img_width/2] = cv2.resize(resized_image, (calc_width, calc_height)) 
	#print "Blank2",blank_image.shape

	new_point_x = int(larger_width/2-scaled_img_width/2+new_point_x)
	new_point_y = int(larger_height/2-scaled_img_height/2+new_point_y)

	#print new_point_x
	#print new_point_y
	#print new_point_y-window_height/2,new_point_y+window_height/2,new_point_x-window_width/2,new_point_x+window_width/2

	start_y = new_point_y-window_height/2
	end_y = new_point_y+window_height/2

	start_x = new_point_x-window_width/2
	end_x = new_point_x+window_width/2
	#print "x",start_x,end_x
	#print "y",start_y,end_y
	#print start_y,end_y,start_x,end_x



	crop_img = blank_image[start_y:end_y,start_x:end_x]
	#print "Cropped shape" , crop_img.shape

	cv2.imshow('dst_rt', crop_img)
	cv2.waitKey(int(1000/frames_per_sec))
	#print "----"
cv2.destroyAllWindows()

exit()
for x in range(1,200):
	resize_x = int(1920*(1+x/100.0))
	resize_y = int(1080*(1+x/100.0))
	resized_image = cv2.resize(img, (resize_x,resize_y)) 
	point_x = 960*resize_x/1920
	point_y = 540*resize_y/1080

	window_width = 800
	window_height = 600

	
	crop_img = resized_image[point_y-window_height/2:point_y+window_height/2,point_x-window_width/2:point_x+window_width/2]
	print crop_img.shape
	cv2.imshow('dst_rt', crop_img)
	cv2.waitKey(20)

cv2.destroyAllWindows()


exit()