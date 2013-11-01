#! /usr/bin/env python

from PIL import Image
from array import array
import sys

if len(sys.argv) < 2:
	sys.exit("Need parameter. Letter. e.g. './char.py d'")
print("Letter: " + sys.argv[1])

img_size = 40
letter = sys.argv[1]
level_of_acceptance = 100;



# load image
img_filename = "40x40/"+ letter +".tif"
img = Image.open(img_filename)

array_img = array('c')

pixels = img.load() # create the pixel map

# save to array
for i in range(img.size[0]):
    for j in range(img.size[1]):
        color = None
	red = pixels[i,j][0]
	green = pixels[i,j][1]
	blue = pixels[i,j][2]
	if red < level_of_acceptance:
		color = True
	elif green < level_of_acceptance:
		color = True
	elif blue < level_of_acceptance:
		color = True
	if color:
		array_img.append('1')
	else:
		array_img.append('0')

# save to file
with open('40x40mono/'+letter+'_array.txt', 'wb') as f:
	array_img.tofile(f)
f.closed


# read from file
array_img2 = array('c')
with open('40x40mono/'+letter+'_array.txt', 'rb') as f:
	array_img2.fromfile(f, img_size*img_size)
f.closed


# recreate a image
img = Image.new( 'RGB', (img_size, img_size)) 

pixels = img.load()
if array_img2[0] != '0':
	print(array_img2)
for i in range(img.size[0]): 
    for j in range(img.size[1]):
	if array_img[(i*40)+j] == '1':
        	pixels[i,j] = (0,0,0)
	else:
		pixels[i,j] = (255,255,255)
img.show()

# new image
img.save('40x40mono/new_' + letter + '.tif')

