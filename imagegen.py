import glob
import random
from PIL import Image, ImageDraw, ImageFont
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os, copy
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image
import argparse
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument("-x",
                    help="Width", 
                    default=512, 
                    type=int, 
                    action="store")
parser.add_argument("-y",
                    help="Height", 
                    default=512, 
                    type=int, 
                    action="store")
parser.add_argument("-n", "--num_neurons",
                    help="Number of neurons", 
                    default=32, 
                    type=int, 
                    action="store")
parser.add_argument("-l", "--num_layers",
                    help="Number of layers", 
                    default=4, 
                    type=int, 
                    action="store")
parser.add_argument("-c", "--count",
                    help="Number of images to be generated", 
                    default=1, 
                    type=int, 
                    action="store")
parser.add_argument("-f", "--file",
                    help="Name of the quotes file", 
                    default="quotes.txt", 
                    type=str, 
                    action="store")

args = parser.parse_args()

class NN(nn.Module):

    def __init__(self, activation=nn.Tanh, num_neurons=16, num_layers=9):
        """
        num_layers must be at least two
        """
        super(NN, self).__init__()
        layers = [nn.Linear(2, num_neurons, bias=True), activation()]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(num_neurons, num_neurons, bias=False), activation()]
        layers += [nn.Linear(num_neurons, 3, bias=False), nn.Sigmoid()]
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)

def init_normal(m):
    if type(m) == nn.Linear:        
        nn.init.normal_(m.weight)
def gen_new_image(size_x, size_y, save=True, **kwargs):
    net = NN(**kwargs)
    net.apply(init_normal)
    colors = run_net(net, size_x, size_y)
    return colors

def run_net(net, size_x=128, size_y=128):
    x = np.arange(0, size_x, 1)
    y = np.arange(0, size_y, 1)
    colors = np.zeros((size_x, size_y, 2))
    for i in x:
        for j in y:
            colors[i][j] = np.array([float(i) / size_y - 0.5, float(j) / size_x - 0.5])
    colors = colors.reshape(size_x * size_y, 2)
    img = net(torch.tensor(colors).type(torch.FloatTensor)).detach().numpy()
    return img.reshape(size_x, size_y, 3)

def randomfont():
    global fonts
    return random.choice(fonts)

def randomline():
    with open(args.file) as lines:
        lines=lines.read().splitlines()
    return random.choice(lines)

#TODO add unix fonts
fonts = list()
for filepath in glob.iglob('C:\\Windows\\Fonts\\*.ttf'):
    fonts.append(filepath)

image_list=list()

for index in range(args.count):
    image = gen_new_image(args.x, args.y, num_neurons=args.num_neurons, num_layers=args.num_layers)
    image = Image.fromarray(image, 'RGB')
    image_list.append(image)

count=0

for image in image_list:
    image_size = image.size
    w = image.size[0]
    h = image.size[1]
    draw = ImageDraw.Draw(image)
    fontname=randomfont()
    font = ImageFont.truetype(fontname, size=64)
    text = randomline()
    lines = textwrap.wrap(text, width=len(text)//3+3)

    while (len(lines)!=3):   
        text = randomline()
        lines = textwrap.wrap(text, width=len(text)//3+3)

    y_text = h
    y_move=[-1.5,-0.5,0.5,1.5]
    i=0 # not very pythonic, i am originally a c++ developer

    for line in lines:
        height=0
        height+=font.getsize(line)[1]

    for line in lines:
        width=font.getsize(line)[0]
        draw.text(((w - width) / 2 -1, (y_text)/2+y_move[i]*height -1), 
            line,
            fill='black', 
            font=ImageFont.truetype(fontname, size=64))
        draw.text(((w - width) / 2 +1, (y_text)/2+y_move[i]*height -1), 
            line,
            fill='black', 
            font=ImageFont.truetype(fontname, size=64))
        draw.text(((w - width) / 2 -1, (y_text)/2+y_move[i]*height +1), 
            line,
            fill='black', 
            font=ImageFont.truetype(fontname, size=64))
        draw.text(((w - width) / 2 +1, (y_text)/2+y_move[i]*height +1), 
            line,
            fill='black', 
            font=ImageFont.truetype(fontname, size=64))
        draw.text(((w - width) / 2, (y_text)/2+y_move[i]*height), 
            line,
            fill='white', 
            font=ImageFont.truetype(fontname, size=64))
        i+=1
        
    image.save("imwithtext%s.jpg"%(str(count)), "JPEG")
    count+=1