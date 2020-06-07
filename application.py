import os

from flask import Flask, session, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = 'myverysecretkey'

socketio = SocketIO(app)

logged_users = ['will', 'celia', 'hugo', 'colin', 'flo']
channels = []
temp_channels = {}

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
        # Make sure the user is in the logged users
        if not dname in logged_users:
            logged_users.append(dname)

        # Create a temporary channel for the user to make if it is not already there
        if not dname in temp_channels:
            temp_channels.update({dname : {'name' : None,
                                            'users' : [dname]}})

        channel_users = temp_channels[dname]['users']
        return render_template("channel_list.html", dname = dname, channels = channels, channel_users = channel_users, users = logged_users)

@app.route("/create_channel")
def create_channel():
    dname = session.get('dname')
    if dname is None:
        return redirect(url_for('index'))
    else:
        return render_template("create_channel.html", dname = dname, channel_users = temp_channels[dname]['users'], channels = channels)

@app.route("/get_users", methods = ['POST'])
def get_users():
    user = request.form.get('user')
    dname = session['dname']
    # If a user is sent, update the channel users.
    print(user)
    if not user == 'No User':
        # Create a temporary channel for the user to make if it is not already there
        if not dname in temp_channels:
            temp_channels.update({dname : {'name' : None,
                                            'users' : [dname]}})
        if user in temp_channels[dname]['users']:
            temp_channels[dname]['users'].pop(temp_channels[dname]['users'].index(user))
        else:
            temp_channels[dname]['users'].append(user)
    return jsonify({'dname' : dname, 'users' : temp_channels[dname]['users']})
