from flask import Flask
from flask import render_template
import os
from StoreNovelData import StoreNovelData

app = Flask(__name__)

@app.route("/")
def index():
    db = StoreNovelData('App.db')
    table_name = 'Webnovels'
    db.select_table(table_name)
    entries = db.dump_table_to_list()
    entries = [(f'{str(i + 1)}.',) + j for i, j in enumerate(entries)] # add numbering to first col
    
    return render_template('index.html', title_name = table_name, entries = entries)