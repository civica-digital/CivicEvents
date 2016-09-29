"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import pickle
import pandas as pd
from pymongo import MongoClient, ASCENDING
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

import tools

app = Flask(__name__)

client = MongoClient()
db = client.log

apiKey= os.environ.get('API_KEY')
allowedIPsFile = "allowedips.p"

if os.path.isfile(allowedIPsFile):
    allowedIPs = pickle.load( open( allowedIPsFile, "rb" ) )
else:
    allowedIPs = []


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.route('/event')
def event():
    """Saves an event on the database."""
    pid = request.args.get('pid')
    event = request.args.get('event')
    date = datetime.now()
    eventDoc = {"pid":pid, "event":event, "date":date}
    db.events.insert(eventDoc)
    return jsonify({'success':"True"}), 200

@app.route('/allowIP')
def allowIP():
    """Adds an IP in the allowed list to send events"""
    sent_apikey = request.args.get('apikey')
    if sent_apikey == apiKey:
        allowedIPs.append(request.remote_addr)
        pickle.dump( allowedIPs, open( allowedIPsFile, "wb" ) )
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/timeline')
def timeline():
    pid = request.args.get('pid')
    event = request.args.get('event')
    period = request.args.get('period')
    if event:
        log = list(db.events.find({"event":event, "pid":pid}).sort("date", ASCENDING))
    else:
        log = list(db.events.find({"pid":pid}).sort("date", ASCENDING))
        event = "all"
    aggregatedLog = tools.aggregate_time(period,log)
    responseDict = {"event":event, "pid":pid, "log":aggregatedLog}
    return jsonify(responseDict), 200


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
