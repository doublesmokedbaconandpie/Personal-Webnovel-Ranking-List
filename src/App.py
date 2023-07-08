from flask import Flask, request
from flask import render_template
import os

from StoreNovelData import StoreNovelData
from NovelEntry import NovelEntry

app = Flask(__name__)

@app.route("/")
def index():
    table_name = 'Webnovels'
    db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
    db.select_table(table_name)
    
    entries = db.dump_table_to_list()
    return render_template('index.html', title_name = table_name, entries = entries)

@app.route('/editCell', methods=['POST', 'GET'])
def saveEditCell():
    if request.method == 'POST':
        db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
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
        if val == db.fetch_entry('ID', id)[0].return_tuple_from_vals()[col_num]:
            return {'result': 'false', 'error': 'DB not updated'}
        
        server_col = NovelEntry.conv_web_col_to_server_col(col)
        db.update_entry(id, server_col, val)
        db.update_entry(id, 'DateModified', date_val)
        return {'result': 'true'} 

@app.route('/fetchScrapedRow', methods=['POST'])
def fetchScrapedRow():
    if request.method == 'POST':
        db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
        table_name = 'Webnovels'
        db.select_table(table_name)
        
        post_json = request.get_json()
        url, id = post_json['url'], int(post_json['id'])
        if id > db.id_tracker.max_ID + 1:
            return {'result': 'false', 'error': 'Invalid ID'} 
        elif id == db.id_tracker.max_ID + 1:
            scrape_url = db.add_entry_from_url(url)
        else:
            scrape_url = db.update_entry_from_url(id, url)
        
        if not scrape_url:
            return {'result': 'false', 'error': f"Scraping url: [{url}] failed"} 
        
        data = db.fetch_entry('ID', id)[0]
        return {'result': 'true',
                'url': data.url,
                'country': data.country,
                'title': data.title,
                'genre': data.genre,
                'tags': data.tags,
                'date_modified': data.date_modified,
                'id': data.id} 