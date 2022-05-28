from flask import Flask,render_template,request,redirect    
import requests
import threading

app = Flask(__name__)

# API keys  

headers = {
    	"X-RapidAPI-Host": "host name",
    	"X-RapidAPI-Key": "API Key"
    }



def stock(name): # Fetch stock data enterd by user
    url = "https://google-finance4.p.rapidapi.com/search/"

    querystring = {"q":name,"hl":"en"}


    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def market_index(): # Fetch market Indexes
    url = "https://google-finance4.p.rapidapi.com/market-trends/"

    querystring = {"t":"indexes","hl":"en"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()



@app.route("/")
def index():
    # market_index
    threading.Thread(target=market_index)
    data = market_index()
    #S&P
    sp = data[0]["items"][0]
    #dowjones
    dowjones = data[0]["items"][1] 
    #sensex
    sensex_data = data[2]["items"][3]
    #nifty
    nifty = data[2]["items"][4]

    return render_template("index.html",sp =sp, dow = dowjones,sensex = sensex_data,nifty= nifty)

# threading is used for boost perfomance while running 

@app.route("/stock", methods = ['POST','GET'])
def data():
    if request.method == 'POST':
        stock_name = request.form['stock_name']     # User Entered Stock Name
        threading.Thread(target=stock_name)
        data = stock(stock_name)                    # calling stock function
        info = data[0]["info"]                      # stock data
        price = data[0]["price"]
    
    threading.Thread(target=market_index)
    data = market_index()       # calling market_index function
    #S&P
    sp = data[0]["items"][0]
    #dowjones
    dowjones = data[0]["items"][1] 
    #sensex
    sensex_data = data[2]["items"][3]
    #nifty
    nifty = data[2]["items"][4]

    return render_template("searched.html",sp =sp, dow = dowjones,sensex = sensex_data,nifty= nifty,info=info,price=price)


app.run(debug=True)