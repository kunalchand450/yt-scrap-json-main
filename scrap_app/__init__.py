import os, tempfile, json
import subprocess
from scrapy.crawler import CrawlerRunner
# json
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
import time
BASE_DIR="/opt/disc_wt/"
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
        # DATABASE=os.path.join(app.instance_path, 'scrap_app.sqlite'),   # Default configuration settings for flask app shoud be changed with frontend lib
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        # Returns index.html file in templates folder.
        return render_template("index.html")

    # After clicking the Submit Button FLASK will come into this
    @app.route('/',methods=['POST'])
    def submit():
        if request.method == 'POST':
            spider_scraps = ['amazon', 'flipkart']
            api_scraps = ['youtube']
            global input_url_final
            input_url_final = []
            input_url = request.form['url']  # Getting the Input Amazon Product URL
            input_url_list = input_url.split(',')
            for url in input_url_list:
                input_url_final.append(url.strip())
            # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
            if os.path.exists(os.path.join(tempfile.gettempdir(),'output.json')):
                os.remove(os.path.join(tempfile.gettempdir(),'output.json'))
            if os.path.exists(os.path.join(tempfile.gettempdir(),'output.csv')):
                os.remove(os.path.join(tempfile.gettempdir(),'output.csv'))

            with open(os.path.join(tempfile.gettempdir(),'start_urls.json'), 'w') as writeurlobj: # here start_urls.json file will be created in write mode
                json.dump({'urls':input_url_final}, writeurlobj)  #this command write the final input in json format which we give from frontend
            # conditions for Amazon and Flipkart
            if request.form['website'] in spider_scraps:  #if we choose amazon here the website will amaxon scrapper or flipkart scrapper
                subprocess.run(["mv", f"/root/crawlerenv/files/webscraper.cfg", "/root/.scrapy.cfg"]) #move Webscrapper.cfg file from crawlerenv to root due to scrapy arch will look root folder first 
                subprocess.run(["scrapy", "crawl", "-O", os.path.join(tempfile.gettempdir(),'output.csv'), "-t", "csv", f"{request.form['website']}spider"]) #this is command for run scrapy file with template crwal and type csv.

            # condition to select and run youtube api scraper    
            if request.form['website'] in api_scraps: # this will select youtube scrapper from option
                subprocess.run(["python3", f"{request.form['website']}_api_scraper.py", "-i", request.form['url'], "-a", request.form['auth_key']])
            
            return send_file(os.path.join(tempfile.gettempdir(),'output.csv'))    
                    
    return app  #start the app again
