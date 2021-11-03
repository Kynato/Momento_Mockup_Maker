# IMPORTS
from genericpath import isdir
from os.path import isfile, join
from collections import namedtuple
from os import listdir, mkdir, remove, startfile

from PIL import Image, ImageDraw
from pdf2image import convert_from_path


# CONSTANTS
LABEL_PATH = 'DROP NEW LABELS HERE/'
LABEL_TEMP_PATH = 'TEMPORARY/'
OUTPUT_PATH = 'OUTPUT/'
TRIM = 42
CORNER_RADIUS = 25

# SMALL BAG CONSTANTS -> make it tuple?
SMALL_BAG_LABEL_OFFSET = (2506, 2332)
SMALL_BAG_PREFIX = 'TEMPLATES/250g/'
SMALL_BAG_BASE = SMALL_BAG_PREFIX + 'base.png'
SMALL_BAG_EFFECTS = SMALL_BAG_PREFIX + 'post.png'

# BIG BAG CONSTANTS -> make it tuple?
BIG_BAG_LABEL_OFFSET = (2548, 2135)
BIG_BAG_PREFIX = 'TEMPLATES/1000g/'
BIG_BAG_BASE = BIG_BAG_PREFIX + 'base.png'
BIG_BAG_EFFECTS = BIG_BAG_PREFIX + 'post.png'

LABEL_SIZE = (1625, 1160)

# Converts PDF->IMG
def images_from_pdfs(pdf_paths):
    if not isdir(LABEL_TEMP_PATH):
        print('Creating TEMPORARY directory for labels... ', end='')
        mkdir(LABEL_TEMP_PATH)
        print('DONE')

    for path in pdf_paths:
        label = convert_from_path(LABEL_PATH + path)
        label[0].save(LABEL_TEMP_PATH + path[:-4] + '.png', 'PNG')

# stolen from stackoverflow idk xd
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

# opens labels, cropps and resizes. Then returns all of them.
def trim_labels():
    print('TRIMMING pdfs... ', end='')
    labels = [f for f in listdir(LABEL_TEMP_PATH) if isfile(join(LABEL_TEMP_PATH,f))]
    cropped_labels = {}
    print(labels)
    for label in labels:
        f = Image.open(LABEL_TEMP_PATH + label)
        f = f.crop((TRIM, TRIM, f.size[0] - TRIM, f.size[1] - TRIM))
        f = f.resize(LABEL_SIZE, resample=Image.BICUBIC)
        f = add_corners(f, CORNER_RADIUS)
        cropped_labels[label] = f
    print('DONE')
    return cropped_labels

# Generates mockups of 250g bags
def mockup_250g_bags(labels:dict):
    small_bag_img = Image.open(SMALL_BAG_BASE).convert('RGBA')
    small_bag_post = Image.open(SMALL_BAG_EFFECTS).convert('RGBA')
    
    for name, label in labels.items():
        print('Generating 250g for: ' + name + '... ', end='')
        label_holder_template = Image.new('RGBA', small_bag_img.size)
        label_holder_template.paste(label, SMALL_BAG_LABEL_OFFSET)
        #label_holder_template.show()
        out = Image.alpha_composite(small_bag_img, label_holder_template)
        out = Image.alpha_composite(out, small_bag_post)
        out.save(OUTPUT_PATH + '250_' + str(name))
        print('DONE')

# Generates mockups of 1000g bags
def mockup_1000g_bags(labels:dict):
    big_bag_img = Image.open(BIG_BAG_BASE).convert('RGBA')
    big_bag_post = Image.open(BIG_BAG_EFFECTS).convert('RGBA')
    
    for name, label in labels.items():
        print('Generating 1000g for: ' + name + '... ', end='')
        label_holder_template = Image.new('RGBA', big_bag_img.size)
        label_holder_template.paste(label, BIG_BAG_LABEL_OFFSET)
        #label_holder_template.show()
        out = Image.alpha_composite(big_bag_img, label_holder_template)
        out = Image.alpha_composite(out, big_bag_post)
        out.save(OUTPUT_PATH + '1000_' + str(name))
        print('DONE')

# Check if folder exists and deletes contents
def clear_temp_folder():
    if isdir(LABEL_TEMP_PATH):
        filelist = [ f for f in listdir(LABEL_TEMP_PATH)]
        for f in filelist:
            remove(join(LABEL_TEMP_PATH, f))  
    
# Returns a list of pdf label files
def list_all_label_files():
    files = [f for f in listdir(LABEL_PATH) if isfile(join(LABEL_PATH,f))]
    print('FOUND {file_count} labels listed below.'.format(file_count = len(files)))
    print('\n'.join(files))
    
    return files



# MAIN MAIN MAIN

# Discover all the labels
label_files = list_all_label_files()

images_from_pdfs(label_files)
labels = trim_labels()

print('GENERATING MOCKUPS...')
mockup_250g_bags(labels)
mockup_1000g_bags(labels)

clear_temp_folder()

startfile('OUTPUT')

