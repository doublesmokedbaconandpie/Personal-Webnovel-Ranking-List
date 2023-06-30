from flask import Flask
from flask import render_template
import os

from StoreNovelData import StoreNovelData
from NovelEntry import NovelEntry

app = Flask(__name__)

@app.route("/")
def index():
    db = StoreNovelData('App.db')
    table_name = 'Webnovels'
    db.select_table(table_name)
    contents = db.dump_table_to_list()
    entries = []
    for i, entry in enumerate(contents):
        tmp = NovelEntry(number = str(i + 1) + '.',
                         country = entry[1],
                         title = entry[2],
                         url = entry[0],
                         chapters_completed = entry[3],
                         rating = entry[4],
                         reading_status = entry[5],
                         genre = entry[6],
                         tags = entry[7],
                         date_modified = entry[8],
                         notes = entry[9])
        entries.append(tmp)
    
    return render_template('index.html', title_name = table_name, entries = entries)