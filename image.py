import cv2
import numpy as np


img = cv2.imread('2.jpg')

blank_image = np.zeros((600,800,3), np.uint8)
resized_image = cv2.resize(img, (320, 240)) 

blank_image[180:420,240:560] = resized_image
cv2.imshow('dst_rt', blank_image)
cv2.waitKey(0)

cv2.destroyAllWindows()

exit()

sec = 30
frames_per_sec = 60.0
frames = sec*frames_per_sec


orig_x = 960
orig_y = 540


dest_x = 534
dest_y = 300


delta_x = dest_x - orig_x
delta_y = dest_y - orig_y

rate_x = delta_x*1.0/frames
rate_y = delta_y*1.0/frames

blank_image = np.zeros((1920*2+100,1080*2+100,3), np.uint8)


for x in range(0,int(frames)):
	resized_image = cv2.resize(img, (1920, 1080)) 
	point_x = orig_x+rate_x*x
	point_y = orig_y+rate_y*x


	print point_x,point_y,x+1


	window_width = 800
	window_height = 600

	
	crop_img = resized_image[point_y-window_height/2:point_y+window_height/2,point_x-window_width/2:point_x+window_width/2]
	print crop_img.shape
	cv2.imshow('dst_rt', crop_img)
	cv2.waitKey(int(1000/frames_per_sec))

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