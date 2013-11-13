#! /usr/bin/env python

from PIL import Image
from array import array
import random

FOLDER_IN='40x40/'
FOLDER_OUT='40x40mono/'
IMG_SIZE=40
IMG_TYPE='.tif'
LEVEL_OF_ACCEPTANCE = 100;

def save_array_to_file(array_img, letter, type_of_noise):
	with open(FOLDER_OUT+letter+type_of_noise+'_array.txt', 'wb') as f:
		array_img.tofile(f)
	f.closed

def read_array_from_file(letter, type_of_noise):
	array_img = array('c')
	with open(FOLDER_OUT+letter+type_of_noise+'_array.txt', 'rb') as f:
		array_img.fromfile(f, IMG_SIZE*IMG_SIZE)
	f.closed
	return array_img

def load_image(letter, tag):
	img_filename = FOLDER_IN + letter + tag + IMG_TYPE
	img = Image.open(img_filename)
	return img

def img_to_mono_array(img):
	array_img = array('c')

	pixels = img.load() # create the pixel map

	# save to array
	for i in range(img.size[0]):
	    for j in range(img.size[1]):
		color = None
		red = pixels[i,j][0]
		green = pixels[i,j][1]
		blue = pixels[i,j][2]
		if red < LEVEL_OF_ACCEPTANCE:
			color = True
		elif green < LEVEL_OF_ACCEPTANCE:
			color = True
		elif blue < LEVEL_OF_ACCEPTANCE:
			color = True
		if color:
			array_img.append('1')
		else:
			array_img.append('0')
	
	return array_img

def save_array_as_img(array_img, letter, type_of_noise):
	img = Image.new( 'RGB', (IMG_SIZE, IMG_SIZE)) 

	pixels = img.load()

	for i in range(img.size[0]): 
	    for j in range(img.size[1]):
		if array_img[(i*IMG_SIZE)+j] == '1':
			pixels[i,j] = (0,0,0)
		else:
			pixels[i,j] = (255,255,255)
	img.save(FOLDER_OUT+ 'new_' + letter + type_of_noise + IMG_TYPE)

def add_noise_remove_line(array, number_of_lines):
	for i in range(number_of_lines):
		white_line = random.randint(0, IMG_SIZE-1)
		for i in range(IMG_SIZE):
			array[(IMG_SIZE*i)+white_line] = '0'
	return array

def add_white_noise(array, percent):
	all_pixels = IMG_SIZE*IMG_SIZE
	pixels_to_change = (all_pixels*percent)/100
	for i in range(pixels_to_change):
		random_x = random.randint(0,all_pixels-1)
		if(array[random_x] == '1'):
			array[random_x] = '0'
		else:
			array[random_x] = '1'
	return array



