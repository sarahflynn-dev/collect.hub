from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key="collector bollector edition remission"

bcrypt = Bcrypt(app)