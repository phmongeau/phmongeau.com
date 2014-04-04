#!/usr/bin/env python

import os
import glob
from PIL import Image

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import json


size = (1280, 720)
def make_thumb(infile, basepath):
    name, ext = os.path.splitext(infile)
    im = Image.open(os.path.join(basepath,infile))
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(os.path.join(basepath, "thumbs/",infile), "JPEG")


basepath = "images/portfolio"
images = [f for f in os.listdir(basepath)
         if os.path.isfile(os.path.join(basepath,f))
         and os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg', '.png')]

print("generating thumbnails:")
for i in images:
    print(os.path.join(basepath, i))
    make_thumb(i, basepath)


img_paths = sorted(images)
img_paths = [i for i in img_paths if not i.endswith(".json")]

with open("images/portfolio/captions.json", "r") as f:
    captions = json.load(f)

template_images = ((os.path.join("images/portfolio", i), os.path.join("images/portfolio/thumbs", i), captions.get(i, "")) for i in img_paths)

loader = FileSystemLoader('templates')
env = Environment(loader=loader)
t = env.get_template('index.html')
with open("index.html", "w") as f:
    f.write(t.render(images=template_images))
