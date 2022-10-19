python3 -m pip install virtualenv
cd /root/
# put your html link and edit this below command before running this project
git clone https://github.com/kunalchand450/yt-scrap-json-main.git
cp -r yt-scrap-json-main/* .
#!/usr/bin/bash
deactivate
cd /root/
# initialize virtualenv
python3 -m virtualenv crawlerenv
# copy scrap_app and amazonscrap to site-packages of virtualenv
cp -r /root/scrap_app/ /root/scrappers/*  /root/crawlerenv/lib/python3*/site-packages/
# add scrapy configurations to crawlerenv
mkdir -p crawlerenv/files/
cp /root/scrapy_cfg/* crawlerenv/files/
# remove scrap_app and amazonscrap to avoid ambiguity(confusion) for flask and scrapy
rm -rf scrappers
# activate virtualenv
source crawlerenv/bin/activate
# install flask scrapy and scrapy user agents
pip install flask scrapy scrapy-user-agents pandas google-api-python-client jsoncsv
rm -rf scrap_app
# tell flask the app names
a2enmod proxy_http
rm -rf /etc/apache2/site-enabled/*
cp scrap_app.conf /etc/apache2/sites-enabled/
service apache2 restart
export FLASK_APP='scrap_app'
# start flask app
echo running flask app
flask run --host="0.0.0.0"
