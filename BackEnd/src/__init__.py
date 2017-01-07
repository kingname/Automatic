from mongoengine import connect
from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

connect(app.config['DB_NAME'])