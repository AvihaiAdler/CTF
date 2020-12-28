from flask import Flask
from ctf.controller import Songs, Secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
data = Songs()
admin = Secrets()

from ctf import view
