from flask import Flask, render_template, redirect, url_for, request, flash, request, session, abort

#from functions import *
import json
import os



app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/', methods=["POST", "GET"])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        if request.method == "POST":

            addr = request.form['apikey']
            privy = request.form['apisecret']

            pair = request.form['buy_percentage']
            percentUP = float(request.form['sell_percentage'])
            marketside = request.form['percent_range']
            total   = float(request.form['fixedbuy'])
            max_price = float(request.form['max_daily_trades'])
            
            #print("Recieved parameters {}: {} \n {}: {} \n {}: {} \n {}: {} \n {}: {} \n {}: {} \n {}: {} \n".format(addr,type(addr), privy,type(privy), pair,type(pair), percentUP,type(percentUP), marketside,type(marketside), total,type(total), max_price, type(max_price)))
            bot = TopOrderBot(addr, privy, pair, percentUP, marketside, total, max_price)
            bot.TopOrderBook()

        return render_template('/index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'ARBbot' and request.form['username'] == 'PJ':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect('/')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'logged_in' in session and session['logged_in']:
        session['logged_in'] = False
    return home()

@app.route('/logs.json', methods=['GET'])
def getLatestLog():
    if session.get('logged_in'):
        #print("Retrieving logs...")
        return json.dumps(readJson('logs'))

    else:
        return render_template('login.html')

@app.route('/clearlogs', methods=['GET'])
def clearLogs():
    if session.get('logged_in'):
        jsonWrite('logs', {})
        return '{}'

    else:
        return render_template('login.html')




if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, threaded=True)
