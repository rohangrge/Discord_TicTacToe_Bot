#!/usr/bin/env python
# coding: utf-8

def initial():
    from PIL import Image  
    img0 = Image.open(r"Green grid.png")
    img1 = Image.open(r"cross white.png")
    img2 = Image.open(r"circle white.png") 
    imar=[img1,img2]
    w=131;h=129
    Pos=[(0,0),(w,0),(2*w,0), (0,h),(w,h),(2*w,h),(0,2*h),(w,2*h),(2*w,2*h)]
  
def render(pos, piece):
    img0.paste(imar[piece], Pos[pos], mask = imar[piece])
    img0.show()






