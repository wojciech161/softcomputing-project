#! /usr/bin/env python

import character

characters = [ 'd', 'g', 'k', 'o', 'r', 's', 'u', 'w' ]

percents = [ 1, 2, 5, 10, 20, 30, 40, 50 ]

numbers = [ 1, 2, 3, 5, 8, 13, 21 ]

def create_character(letter,file_tag):
	img = character.load_image(letter, file_tag)
	array_img = character.img_to_mono_array(img)
	character.save_array_to_file(array_img, letter, file_tag)
	character.save_array_as_img(array_img, letter, file_tag)

def create_character_white_noise(letter, file_tag, percent):
	file_tag = file_tag + str(percent)
	array_img = character.read_array_from_file(letter, '')
	character.add_white_noise(array_img, percent) # percent
	character.save_array_to_file(array_img, letter, file_tag)
	character.save_array_as_img(array_img, letter, file_tag)

def create_character_noise_remove_line(letter, file_tag, number):
	file_tag = file_tag + str(number)
	array_img = character.read_array_from_file(letter, '')
	character.add_noise_remove_line(array_img, number) # number of lines
	character.save_array_to_file(array_img, letter, file_tag)
	character.save_array_as_img(array_img, letter, file_tag)

def main():
	for letter in characters:
		create_character(letter, '') # Times New Roman
		create_character(letter, '_s') # Serif
		create_character(letter, '_a') # Arial
		for percent in percents:
			create_character_white_noise(letter, '_w', percent)
		for number in numbers:
			create_character_noise_remove_line(letter, '_rl', number)

if __name__ == "__main__":
    main()
