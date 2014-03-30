#!/usr/bin/env python

import os
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

loader = FileSystemLoader('templates')
env = Environment(loader=loader)


images = sorted(os.listdir("images/portfolio"), reverse=True)
images = ["images/portfolio/{}".format(i) for i in images]

# TODO
captions = [""] * len(images)

t = env.get_template('index.html')
with open("index.html", "w") as f:
    f.write(t.render(images=zip(images, captions)))
