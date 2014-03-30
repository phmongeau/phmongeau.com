#!/usr/bin/env python

import os
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import json

loader = FileSystemLoader('templates')
env = Environment(loader=loader)


img_paths = sorted(os.listdir("images/portfolio"), reverse=True)
img_paths = [i for i in img_paths if not i.endswith(".json")]

# TODO
with open("images/portfolio/captions.json", "r") as f:
    captions = json.load(f)

images = ((os.path.join("images/portfolio", i), captions.get(i, "")) for i in img_paths)

t = env.get_template('index.html')
with open("index.html", "w") as f:
    f.write(t.render(images=images))
