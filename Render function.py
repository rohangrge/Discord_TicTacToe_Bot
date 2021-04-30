#!/usr/bin/env python
# coding: utf-8

from PIL import Image

'''img0 = Image.open(r"Green grid.png")
img1 = Image.open(r"cross white.png")
img2 = Image.open(r"circle white.png")
imar = [img1, img2]
w = 131
h = 129
Pos = [[(0, 0), (w, 0), (2*w, 0)],
       [(0, h), (w, h), (2*w, h)],
       [(0, 2*h), (w, 2*h), (2*w, 2*h)]]'''

arr = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]


def render(garray):
    img0 = Image.open(r"Green grid.png")
    img1 = Image.open(r"cross white.png")
    img2 = Image.open(r"circle white.png")
    imar = [img1, img2]
    w = 131
    h = 129
    Pos = [[(0, 0), (w, 0), (2*w, 0)],
           [(0, h), (w, h), (2*w, h)],
           [(0, 2*h), (w, 2*h), (2*w, 2*h)]]
    a = 0
    for i in garray:
        b = 0
        for j in i:
            if(j == -1):
                b += 1
            else:
                img0.paste(imar[j], Pos[a][b], mask=imar[j])
                #img0.save("Green grid.png")
                # img0.show()
                b += 1
        a += 1
    img0.show()


render(arr)
