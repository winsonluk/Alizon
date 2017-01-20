from itertools import izip
from PIL import Image
import time
import math, operator

def comp_imgs(im1, im2):
    i1 = im1.convert('RGB')
    i2 = im2.convert('RGB')
    print i1.size, i2.size
    i1 = i1.resize((200, 200), Image.ANTIALIAS)
    i2 = i2.resize((200, 200), Image.ANTIALIAS)
    print i1.size, i2.size

    h1 = i1.histogram()
    h2 = i2.histogram()

    rms = math.sqrt(reduce(operator.add,
        map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

    #i1.save("temp1.png", "PNG")
    #i2.save("temp2.png", "PNG")

    print rms

    #a = raw_input()
    return rms

def comp_imgs2(im1, im2):
    i1 = im1.convert('RGB')
    i2 = im2.convert('RGB')
    i1.resize((400,400))
    i2.resize((400,400))
    #print 'SIZE'
    #print i1.size, i2.size

    i1.save("temp1.png", "PNG")
    i2.save("temp2.png", "PNG")
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    print 100 - (dif / 255.0 * 100) / ncomponents
    a = raw_input()
    return 100 - (dif / 255.0 * 100) / ncomponents
