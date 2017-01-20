from aliexpress_api_client import AliExpress
import PIL
from PIL import Image, ImageChops
import urllib2 as urllib
import io
from itertools import izip

from libImgComp import comp_imgs



def comp_images(i1, i2):
    maxsize = (500, 500)
    i1.resize(maxsize)
    i2.resize(maxsize)
    i1 = i1.convert('RGB')
    i2 = i2.convert('RGB')
    return comp_imgs(i1, i2)
    '''pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    return 100 - (dif / 255.0 * 100) / ncomponents'''

import math, operator

def process_str(s):
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('<b>', '')
    s = s.replace('</b>', '')
    s = s.replace('<font>', '')
    s = s.replace('</font>', '')
    s = s.replace('Generic', '')
    s = s.replace(',', '')
    s = s.replace('.', '')
    s = s.replace('-', '')
    s = s.replace('/', '')
    s = s.replace('\\', '')
    s = s.replace('  ', ' ')
    return s

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def strdiff(s1, s2):
   s1 = s1.lower()
   s2 = s2.lower()
   count = 0
   l1 = s1.split(' ')
   for item in l1:
      if (s2.find(item) != -1):
         count += 1

   return count

def get_perc(mi, ma, va):
   if (mi == ma):
      for item in va:
         yield 100.0
   else:
      for item in va:
         yield (((item - mi)/(ma - mi)))*100


def get_perc_w(mi, ma, va):
   if (mi == ma):
      for item in va:
         yield 100.0
   else:
      for item in va:
         n = (item/ma)*100
         yield n

def get_max_ind(a):
   x = max(a)
   for i in range(len(a)):
      if (a[i] >= x - 15):
         yield i

def get_min_ind(a):
   x = min(a)
   for i in range(len(a)):
      if (a[i] <= x + 15):
         return i

def get_m_i(a):
   x = max(a)
   for i in range(len(a)):
      if (a[i] == x):
         return i


def get_avg(st, img):
    return (1.7*st + 0.3*img) / 2.0

def price_float(s):
   return float(s[4:])

def eval_p(prices, or_p):
    for price in prices:
        print str(price) + ' <- PRICE'
        print str(or_p) + ' <- OR_PRICE'
        if (5*price > (or_p - price) and price >= 0.45*or_p):
            print 'GOT ' + str(price)
            yield price

def get_pairs(li):
    for i in range(len(li)-1):
        yield li[i] + ' ' + li[i + 1]

def get_pairs_strict(li):
    for i in range(len(li)/2):
        yield li[2*i] + ' ' + li[2*i + 1]

def get_all_maxs(li):
    m = max(li)
    for i in range(len(li)):
        if li[i] == m:
            yield i

def get_all_mins(li):
    m = min([n for n in li if n>0])
    for i in range(len(li)):
        if li[i] == m:
            yield i

def get_all_maxs_mild(li):
    m = max(li)
    for i in range(len(li)):
        if li[i] >= m - 10:
            yield i

def get_all_mins_mild(li):
    m = min([n for n in li if n>0])
    for i in range(len(li)):
        if li[i] <= m + 10:
            yield i


def process_pr(li, t):
    for i in li:
        if i > t:
            yield -1
        else:
            yield i


def calc_result(s_item, or_price, or_img):
  # print 'starting Daniils part'
   COEFF = 0.7
   s_item = process_str(s_item)
   item_copy = s_item
   aliexpress = AliExpress('YOUR_CODE_HERE')

   '''while (not_working):
       try:
          print ' '.join(s_item.split(' ')[:-count])
          products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], ' '.join(s_item.split(' ')[0:-count]))['products']
          cur_len = len(products)
          print cur_len
          if ((cur_len < old_len or cur_len >= 15) and count >= 3):
              if (cur_len < old_len):
                products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], ' '.join(s_item.split(' ')[0:-(count - 1)]))['products']
              print 'disabling'
              not_working = False
          else:
              raise ValueError('  fff  ')
       except:
           count += 1;
           old_len = cur_len
           if (count + 1 == len(item_copy.split(' '))):
               break
           #print ' '.join(s_item.split(' ')[:count])'''
   done = False
   old_len = 0
   cur_len = 0
   products = {}
   le_s = len(item_copy.split(' '))
   search_query = s_item.split(' ')


   previous_max = 20


   #a = raw_input()
   while (not done):
       count = 0
       print "Going into the next lap"
       print search_query
       lens_titles = []
       lens_values = []
       if (len(search_query) != 1):
           search_query = list(get_pairs(search_query))
       max_count = len(search_query)
       while (count < max_count):
           products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], search_query[count],
                                                  originalPriceFrom=str(or_price*COEFF), sort="orignalPriceUp")['products']
           lens_titles.append(search_query[count])
           lens_values.append(len(products))
           count += 1

       maxs_i = list(get_all_maxs(lens_values))
       print '--------------------------------'
       #print maxs_i
       if (len(maxs_i) == 0 or lens_values[maxs_i[0]] == 0):
           #print maxs_i
           #print lens_values[maxs_i[0]]
           search_query = list(get_pairs_strict(final_search_query))
           print 'Shutting down'
           done = True
       elif (len(maxs_i) == 1 and lens_values[maxs_i[0]] >= 2):
           search_query = [lens_titles[maxs_i[0]]]
           #print maxs_i
           #print lens_values
           print 'Shutting down - one good result'
           done = True
       elif (len(maxs_i) == 1 and lens_values[maxs_i[0]] < 2):
           search_query = list(get_pairs_strict(final_search_query))
           #print maxs_i
           #print lens_values
           print 'Shutting down - one bad result'
           done = True
       else:
           search_query = []
           #print maxs_i
           print 'Keeping on'
           if (len(maxs_i) >= 2 and lens_values[maxs_i[0]] != 0):
                        final_search_query = []
                        for item in maxs_i:
                            k = len(lens_titles[item].split(' '))
                            final_search_query.append(' '.join(lens_titles[item].split(' ')[:k/2]))

                        final_search_query.append(' '.join(lens_titles[-1].split(' ')[k/2+1:]))
                        search_query = list(get_pairs_strict(final_search_query))




   #printing the result
   '''
   for item in search_query:
        products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], item)['products']
        print '----------------------------------------------------------------------'
        print item
        print len(products)
        for i in products:
            print i['productTitle']
   '''
   links = []
   prices = []
   perc = []
   diffs = []
   print search_query
   print 'STARTING CHECK FOR EACH POS ...'
   for s in search_query:
       print 'INPUT:'
       print s
       products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], s,
                                                  originalPriceFrom=str(or_price*COEFF), sort="orignalPriceUp")['products']
       print len(products)
       #a = raw_input()
       l, p, perct, diff = search(products, item_copy, or_price, or_img)
       links.extend(l)
       prices.extend(p)
       perc.extend(perct)
       diffs.extend(diff)




   max_perc = list(get_all_maxs_mild(perc))
   min_prices = list(get_all_mins_mild(prices))

   print 'ORIG PR : ' + str(or_price)
   result = list(set(max_perc).intersection(min_prices))
   print 'MAX PERC:'
   print max_perc
   print 'MIN PRC:'
   print min_prices
   prices = list(process_pr(prices, or_price))
   print prices
   print 'RES:'
   print result

   result_perc = []

   for item in result:
       print links[item]
       print prices[item]
       print perc[item]
       result_perc.append(perc[item])

   if (len(result) != 0):
        final_ind = get_m_i(result_perc)
        fin = result[final_ind]


   #a = raw_input()
   if (len(result) != 0):
       return links[fin], prices[fin], diffs[fin]
   else:
       return links[min_prices[0]], prices[min_prices[0]], diffs[min_prices[0]]



def search(products, s_item, or_price, or_img):
   print 'Starting search...'
   #print len(products)
   #try:
   #print or_img
   fd = urllib.urlopen(or_img)
   orig_img_link = io.BytesIO(fd.read())
   orig_img = Image.open(orig_img_link)



   #except:
   #orig_img_link = cStringIO.StringIO(urllib.urlopen('http://cs617219.vk.me/v617219415/c9c4/KUCX_V8m7CQ.jpg').read())
   #orig_img = Image.open(orig_img_link)

   titles = []
   image_diffs = []
   img_data = []

   #i = 0;
   for item in products:
      #i += 1;
      #img.show()
      #print process_str(item['productTitle'])
      titles.append(process_str(item['productTitle']))
      try:
        #print item['productTitle'] + item['salePrice'] + '\n' + item['imageUrl'] + '\n'
        fd = urllib.urlopen(item['imageUrl'])
        img_link = io.BytesIO(fd.read())
        img = Image.open(img_link)
        #image_diffs.append(rmsdiff(img, orig_img))
        #print comp_images(orig_img, img)
        img_data.append(comp_images(orig_img, img))
        #a = raw_input();
        #print i
        #print '___________________________________________________________________________'
      except:
         img_data.append(50)

   string_diffs = map(strdiff, titles, [s_item]*len(titles))
   max_strdiff = float(max(string_diffs))
  # max_imgdiff = float(max(image_diffs))
   min_strdiff = float(min(string_diffs))
 #  min_imgdiff = float(min(image_diffs))
   #print 'CHECK IMG DATA'
   #print img_data
   #print 'MIN'
   #print min(img_data)
   #print 'MAX'
   #print max(img_data)

   str_data = list(get_perc_w(min_strdiff, max_strdiff, string_diffs))
   img_data = list(get_perc(min(img_data), max(img_data), img_data))

   comp_data = map(get_avg, str_data, img_data)



   #print "word matches: "
   #print str_data
   #print "images:"
   #print img_data
   #print "comp:"
   #print comp_data

   ids = list(get_max_ind(comp_data))

   #print 'IDs'
   #print ids


   urls = []
   prices = []
   percs = []
   diffs = []
   for item in ids:
       urls.append(products[item]['productUrl'])
       prices.append(price_float(products[item]['salePrice']))
       percs.append(comp_data[item])
       diffs.append(or_price - price_float(products[item]['salePrice']))

   print urls
   print prices
   print percs
   print diffs

#'''or (or_price - new_price > 5*new_price) or comp_data[ids[get_min_ind(prices)]] < 50'''

   return urls, prices, percs, diffs


