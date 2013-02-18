#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import flask, flask.views
import os
import functools
app = flask.Flask(__name__)
# Don't do this!!
app.secret_key = 'secret'

users = {'user':'pass'} 
HOST = '127.0.0.1'
# HOST = '192.168.11.16'
PORT = 8000

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    
    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))

class  About(flask.views.MethodView):
    def get(self):
        return flask.render_template('about.html')
            
def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("ページを見るにはログインが必要です!")
            return flask.redirect(flask.url_for('index'))
    return wrapper

class Remote(flask.views.MethodView):
	@login_required	
	def get(self):
		return flask.render_template('remote.html')

	@login_required
	def post(self):
		result = eval(flask.request.form['expression'])
		flask.flash(result)
		return self.get()

class Music(flask.views.MethodView):
    @login_required
    def get(self):
        songs = os.listdir('static/music/')
        return flask.render_template('music.html', songs=songs) 

@app.route('/action/')
def action():
    return flask.render_template('action.html')

app.add_url_rule('/',
				view_func=Main.as_view('index'),
				methods=['GET', 'POST'])
"""
app.add_url_rule('/<page>/', 
                 view_func=Main.as_view('main'),
                 methods=['GET'])
"""

app.add_url_rule('/about/',
                 view_func=About.as_view('about'),
                  methods=['GET'])

app.add_url_rule('/remote/', 
				 view_func=Remote.as_view('remote'), 
				 methods=['GET', 'POST'])

app.add_url_rule('/music/',
                 view_func=Music.as_view('music'), 
                 methods=['GET'])

app.debug = True
app.run(host=HOST, port=PORT)
