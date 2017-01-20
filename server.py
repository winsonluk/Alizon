from flask import Flask
from Alizon import main
import json

app = Flask(__name__)

@app.route("/")
def home():
   return "first page"

@app.route("/getInfo", methods=['POST'])
def getInfo():
   link = request.args['link']
   res = main('https://www.amazon.com/Apple-iPhone-5S-Certified-Refurbished/dp/B00YD53YQU/ref=sr_1_1?s=wireless&ie=UTF8&qid=1484390983&sr=1-1&keywords=iphone')
   return json.dumps({'link':res})
if __name__ == "__main__":
   app.run()
