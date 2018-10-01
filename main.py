from flask import Flask, request, render_template, redirect, url_for, session
import requests
import io
import pandas as pd
import csv
from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side

lme = LightMatchingEngine()

app = Flask(__name__)

# PAGE ROUTES

@app.route("/")
def index():
    return render_template('/homeLanding.html')  

@app.route('/homeLanding')
def home():
    return render_template('/homeLanding.html')

@app.route('/userLanding')
def userLanding():
    return render_template('/userLanding.html')

@app.route('/falseIdent')
def falseIdent():
    return render_template('/homelandingNullLogin.html')

@app.route('/profile')
def profile():
    user_name = session.get('user_name',None)
    return render_template('/extras-profile.html',user_name=user_name)

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/calendar')
def calendar():
     return render_template('calendar.html')

@app.route('/messageBox')
def messageBox():
    return render_template('/email-inbox.html')

# FORM ROUTES

@app.route('/userHome', methods=['GET','POST'])
def userHome():
    user_num = "0"
    user_name = "User"
    if request.method == 'POST':
        user_num = request.form['user_id']
        
    if user_num == "1":
           user_name  = "William"
    else:
        return redirect('/falseIdent')
    session['user_name']= user_name   
    return render_template('/index.html', user_name=user_name)
        
@app.route('/stockQuote', methods=['GET','POST'])
def stockQuote():
    API_KEY = '8XTSMCVVBO5CJLT9'
    if request.method == 'POST':
        stock_request = request.form['stock_search']
        r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey='%stock_request + API_KEY)
        session['stock_request'] = stock_request
        session['stock_data'] = r.text
        with open('out.csv', 'w') as f:
            writer = csv.writer(f)
            reader = csv.reader(r.text)

            for row in reader:
                writer.writerow(row)
        
        stock_data = pd.read_csv('out.csv',error_bad_lines=False)

          
    return render_template('/stockData.html', stock_data=stock_data,stock_request=stock_request)


@app.route('/stockData')
def stockData():
    return
    

@app.route('/buyEntered', methods=['GET','POST'])
def buyEntered():
    if request.method == 'POST':
        stock_request = session.get('stock_request',None)
        stock_data = session.get('stock_data', None)
        order_size = request.form['order_size']
        order_price = request.form['order_price']
       # order_type = request.form['order_type']
       # order, trades = lme.add_order(stock_request, order_price, order_size, Side.BUY)
        order = [stock_request, order_price, order_size, "buy"]
        with open("order.txt","w") as fo:
            fo.writelines(repr(order))

        
        return render_template('/stockData.html', stock_request= stock_request, stock_data = stock_data)




#Functions

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

   
    app.run(debug=True)
    
