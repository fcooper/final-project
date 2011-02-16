from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

with Image() as wand:

	for z in range(1,10):
		with Drawing() as draw:
			draw.stroke_color = Color('black')
			draw.stroke_width = 2
			draw.fill_color = Color('white')
			draw.arc(( 25, 25),  # Stating point
					( 75, 75),  # Ending point
					(13*z,-45))  # From bottom left around to top right


			with Image(width=100,
					height=100,
					background=Color('lightblue')) as img:
				draw.draw(img)
				wand.sequence.append(img)


	for cursor in range(3):
		with wand.sequence[cursor] as frame:
			frame.delay = 10 * (cursor + 1)
		# Set layer type
		wand.type = 'optimize'
		wand.save(filename='animated.gif')




