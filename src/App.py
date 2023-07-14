from flask import Flask, request
from flask import render_template
import os
import logging

from StoreNovelData import StoreNovelData
from NovelEntry import NovelEntry

logging.basicConfig(level=logging.INFO, filename="logger.log", datefmt='%m/%d/%Y %H:%M:%S',
                    format='%(levelname)s: %(module)s: %(message)s; %(asctime)s')
app = Flask(__name__)

@app.route("/")
def index():
    logging.info('Loading index')
    table_name = 'Webnovels'
    db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
    db.select_table(table_name)
    
    entries = db.dump_table_to_list()
    return render_template('index.html', title_name = table_name, entries = entries)

@app.route('/editCell', methods=['POST', 'GET'])
def editCell():
    if request.method == 'POST':
        logging.info('Post request for editCell')
        db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
        table_name = 'Webnovels'
        db.select_table(table_name)
        
        post_json = request.get_json()
        id, col, val, date_val = int(post_json['id']), post_json['col'], post_json['val'], post_json['date_val']
        col_num = NovelEntry.get_col_num(col)
        logging.info(f'id: {id}, col: {col}, val: {val}, date_val: {date_val}, col_num: {col_num}')
        
        if id > db.id_tracker.max_ID + 1:
            return {'result': 'false', 'error': 'Invalid ID'} 
        if not db.exists_entry('ID', id):
            add_success = db.add_entry("Url", None) # placeholder to just add new id for new row
            logging.info(f'Entry for ID: {id} doesnt exist in DB. Creating entry. Success = {add_success}')
        if not NovelEntry.is_valid_col(col):
            return {'result': 'false', 'error': 'Invalid Column'} 
        if val == db.fetch_entry('ID', id)[0].return_tuple_from_vals()[col_num]:
            return {'result': 'false', 'error': 'DB not updated'}
        
        server_col = NovelEntry.conv_web_col_to_server_col(col)
        col_update_success = db.update_entry(id, server_col, val)
        date_update_success = db.update_entry(id, 'DateModified', date_val)
        logging.info(f'Col updated: {col_update_success}, Server_col: {server_col}')
        logging.info(f'Date updated: {date_update_success}')
        return {'result': 'true'} 

@app.route('/fetchScrapedRow', methods=['POST'])
def fetchScrapedRow():
    if request.method == 'POST':
        logging.info('Post request for fetchScrapedRow')
        db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
        table_name = 'Webnovels'
        db.select_table(table_name)
        
        post_json = request.get_json()
        url, id = post_json['url'], int(post_json['id'])
        logging.info(f'url: {url}, id: {id}')
        if id > db.id_tracker.max_ID + 1:
            return {'result': 'false', 'error': 'Invalid ID'} 
        elif id == db.id_tracker.max_ID + 1:
            scrape_url = db.add_entry_from_url(url)
        else:
            scrape_url = db.update_entry_from_url(id, url)
        logging.info(f'Scrape url: {scrape_url}')
        
        if not scrape_url:
            return {'result': 'false', 'error': f"Scraping url: [{url}] failed"} 
        
        data = db.fetch_entry('ID', id)[0]
        logging.info(f'Fetched data: {data}')
        return {'result': 'true',
                'url': data.url,
                'country': data.country,
                'title': data.title,
                'genre': data.genre,
                'tags': data.tags,
                'date_modified': data.date_modified,
                'id': data.id} 

@app.route('/deleteRow', methods=['DELETE'])
def deleteRow():
    if request.method == 'DELETE':
        logging.info('Post request for deleteRow')
        db = StoreNovelData('App.db', 'NovelCache.db', 'Webnovels')
        table_name = 'Webnovels'
        db.select_table(table_name)
        
        post_json = request.get_json()
        id = int(post_json['id'])
        logging.info(f'id: {id}')
        
        delete_attempt = db.delete_entry('ID', id)
        logging.info(f'Delete attempt: {delete_attempt}')
        
        if delete_attempt:
            return {'result': 'true'}
        return {'result': 'false', 'error': 'Invalid ID'} 

if __name__ == "__main__":
    app.debug = False
    app.run()