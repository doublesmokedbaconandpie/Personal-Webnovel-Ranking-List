from flask import Flask, request
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
        tmp = NovelEntry()
        tmp.assign_vals_from_tuple(i, entry)
        entries.append(tmp)
    return render_template('index.html', title_name = table_name, entries = entries)

@app.route('/editCell', methods=['POST', 'GET'])
def testfn():
    if request.method == 'POST':
        db = StoreNovelData('App.db')
        table_name = 'Webnovels'
        db.select_table(table_name)
        
        post_json = request.get_json()
        id, col, val, date_val = int(post_json['id']), post_json['col'], post_json['val'], post_json['date_val']
        col_num = NovelEntry.get_col_num(col)
        
        if id > db.id_tracker.max_ID + 1:
            return {'result': 'false', 'error': 'Invalid ID'} 
        if not db.exists_entry('ID', id):
            db.add_entry("Url", None) # placeholder to just add new id for new row
        if not NovelEntry.is_valid_col(col):
            return {'result': 'false', 'error': 'Invalid Column'} 
        if val == db.fetch_entry('ID', id)[0][col_num]:
            return {'result': 'false', 'error': 'DB not updated'}
        
        server_col = NovelEntry.conv_web_col_to_server_col(col)
        db.update_entry(id, server_col, val)
        db.update_entry(id, 'DateModified', date_val)
        return {'result': 'true'} 
    if request.method == 'GET':
        return {'result': 'true'} 
    