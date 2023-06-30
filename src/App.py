from flask import Flask
from flask import send_from_directory, render_template
import os

print(os.listdir())
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')