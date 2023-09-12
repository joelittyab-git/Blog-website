from flask import Flask
from flask_session import Session
from backend.Database import database
from flask_socketio import SocketIO
from backend.__credentials import(
    USERNAME,
    PASSWORD,
    DATABASE
)

app = Flask(__name__)

#App configurations
app.config['SECRET_KEY'] = '34eecd8d795f5f7e8103e4b974bec7c05b5a'
app.config['UPLOAD_FOLDER'] = 'static/profile_img'
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'


sess = Session(app)
socket = SocketIO(app)

#Database configurations
parent_db = database(
    username = f'{USERNAME}',
    database = f'{DATABASE}',
    password = f'{PASSWORD}',
)

class Constants:
    #Network constants
    port = 1000
    host = 'localhost'
    
    #Database
    username = f'{USERNAME}'
    database = f'{DATABASE}'
    password = f'{PASSWORD}'