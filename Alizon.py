import configparser
from amazon.api import AmazonAPI
from aliexp import calc_result
import cgi, cgitb






def main(selfStr):

  config = configparser.ConfigParser()
  #config.read('config.ini')

  #AMAZON_KEY = config.get('amazon', 'AMAZON_KEY')
  AMAZON_KEY = 'YOUR KEY HERE'
  #AMAZON_SECRET = config.get('amazon', 'AMAZON_SECRET')
  AMAZON_SECRET = 'YOUR SECRET KEY HERE'
  #AMAZON_ASSOCIATE = config.get('amazon', 'AMAZON_ASSOCIATE')
  AMAZON_ASSOCIATE = 'reffit-20'
  amazon = AmazonAPI(AMAZON_KEY, AMAZON_SECRET, AMAZON_ASSOCIATE)



  if ('/dp/' in selfStr) or ('/gp/' in selfStr):
    #try:
      print 'Finding item...'
      product = amazon.lookup(ItemId=get_asin(selfStr))
      print 'Found item!'
      title = product.title
      price = min(product.price_and_currency[0], product.list_price[0])
      if (price <= 0):
          price = max(product.price_and_currency[0], product.list_price[0])

      #print product.images[0].LargeImage.URL
      '''  for im in product.images:
        print im.LargeImage.URL
      a = raw_input() '''
      image = str(product.images[-1].LargeImage.URL)
      print title
      print price
      print image
      print 'Starting calculations'
      link, p, diff = calc_result(title, price, image)

      print link + ' $:' + str(p) + ' ' + str(diff)
      return link, p, diff
    #except:
     # print 'ERROR: PRODUCT NOT FOUND'
    #  return 'ERROR: PRODUCT NOT FOUND', -1, 0
    #else:
    #  print 'ERROR: NOT AMAZON PRODUCT LINK'
     # return 'ERROR: NOT AMAZON PRODUCT LINK', -1, 0

def get_asin(text):
  '''Return Amazon ASIN'''

  if '/dp/' in text:
    start_index = text.find('/dp/') + 4
  elif '/gp/product/' in text:
    start_index = text.find('/gp/') + 12
  elif '/gp/' in text:
    start_index = text.find('/gp/') + 9
  else:
    raise ValueError('ERROR: ASIN NOT FOUND')

  if start_index + 10 > len(text):
    raise ValueError('ERROR: ASIN OUT OF RANGE')
  else:
    asin = text[start_index:start_index+10]
  return asin

