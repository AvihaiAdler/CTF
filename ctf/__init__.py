from flask import Flask
from ctf.controller import Songs, Secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = '4fb8dac4d9aa0e70d016bccc9a2a17d9c5ff161809f11ecfd79d751b446d0f0c'
data = Songs()
admin = Secrets()

from ctf import view