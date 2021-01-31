from flask import Flask,render_template, redirect, url_for, request, session,flash
import requests


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/maps')
def maps():
    r = requests.get('https://xk4w3gnxqb.execute-api.ap-southeast-2.amazonaws.com/beta_0_0/allcountrylocations')
    j = r.json()
    return render_template('maps.html',location = j)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()