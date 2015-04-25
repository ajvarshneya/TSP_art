from PIL import Image

if __name__ == "__main__":
	raw_path = input('Enter image path/name: ')
	# Load / grayscale an image
	img = Image.open(raw_path)
	img_gray = Image.new('L', img.size) # 'L' or 'RGB'

	print("Processing image...")

	width, height = img.size
	pixels = img_gray.load()

	# iterate through horizontal pixels
	for x in range(0, width):
		# iterate through vertical pixels
		for y in range(0, height):
			# get pixel at a particular coordinate
			color = img.getpixel((x,y))
			# convert to gray (weighted avg)
			r, g, b = color
			gray = int(0.2126*r+0.7152*g+0.0722*b)
			# replace pixel in new image
			img_gray.putpixel((x,y), gray) # 'L' format
			# img_gray.putpixel((x,y), (gray,gray,gray)) # 'RGB' format

	print("Complete!")

	img_gray.save('gray.jpg')
	print('Saved grayscaled %s as gray.jpg') % raw_path

	# generate voronoi diagram


