# IMPORTS
from PIL import Image


# CONSTANTS
IMAGE_PATH = 'images/'
BASE_IMG_NAME = IMAGE_PATH + 'x.bmp'
NEW_ETQ_IMG_NAME = IMAGE_PATH + 'face.bmp'
EFFECTS_IMG_NAME = IMAGE_PATH + 'effects.bmp'

# MAIN
base_im = Image.open(BASE_IMG_NAME).convert('RGBA')
new_etq_im = Image.open(NEW_ETQ_IMG_NAME).convert('RGBA')

output_im = Image.alpha_composite(base_im, new_etq_im)

# show the output
output_im.show()
