from PIL import Image

def generate_voronoi_diagram():


if __name__ == "__main__":

	# Load / grayscale an image
	img = Image.open('koala.jpg')
	img_gray = Image.new('L', img.size) # 'L' or 'RGB'

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

	img_gray.show()
	img_gray.save('koala_gray.jpg')

	img_dots = Image.new('')

	# generate voronoi diagram


