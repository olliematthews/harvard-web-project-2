import os

from flask import Flask, session, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

socketio = SocketIO(app)

logged_users = []
channels = []


@app.route("/", methods = ['GET', 'POST'])
def index():
    dname = session.get('dname')
    if dname is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('channel_list'))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    dname = session.get('dname')
    if dname is None:
        if request.method == 'GET':
            return render_template("login.html", messages = [])
        else:
            dname = request.form.get('dname')
            if dname in logged_users:
                message = {'fail' : True,
                            'message' : 'Display name already in use. Pick another.'}
                return render_template("login.html", messages = [message])
            else:
                logged_users.append(dname)
                session['dname'] = dname
                return redirect(url_for('channel_list'))
    else:
        return redirect(url_for('channel_list'))


@app.route("/logout", methods = ['GET'])
def logout():
    session.pop('dname')
    message = {'fail' : False,
                'message' : 'Successfully signed out.'}
    return render_template("login.html", messages = [message])

@app.route("/channel_list")
def channel_list():
    dname = session.get('dname')
    if dname is None:
        return redirect(url_for('index'))
    else:
        return render_template("channel_list.html", dname = dname, channels = channels)

@app.route("/create_channel")
def create_channel():
    dname = session.get('dname')
    if dname is None:
        return redirect(url_for('index'))
    else:
        return render_template("create_channel.html", dname = dname, channels = channels)
