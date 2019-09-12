# webscraper

REST API for scrapping data (text and images) from websites.

# How to run?

1. Clone repository: git clone https://github.com/mzakonek/webscraper.git

## with Docker
2. go into directory with docker-compose.yml file
3. run command: docker-compose up --build -d
4. run command: docker-compose run web /usr/local/bin/python manage.py migrate

In case of problems with accessing Postgres from external ports, check link below:
https://gist.github.com/MauricioMoraes/87d76577babd4e084cba70f63c04b07d


## without Docker
2. cd into webscraper: cd webscraper
3. install requirements: pip install -r requirements.txt
4. run command: python manage.py makemigrations
5. run command: python manage.py migrate
6. download and install Redis, open terminal and run: redis-server
7. open new terminal window, activate our virtual environment and run: celery worker -A webscraper --loglevel=info


# curls
## Pages
create new url record in db

curl -d "url=UrlPageE.G.http://wyborcza.pl" -X POST http://localhost:8000/api/pages/

check details about this url in db

curl -X GET http://localhost:8000/api/pages/PAGEID/

## Text scraper
start process of scrapping text from url

curl -X POST http://localhost:8000/api/textscraper/?urlid=PAGEID

get data scrapped from page

curl -X GET http://localhost:8000/api/textscraper/PAGEID/

## Image scraper
start process of scrapping imgs from url

curl -X POST http://localhost:8000/api/imgscraper/?urlid=PAGEID

get imgs scrapped from page

curl -X GET http://localhost:8000/api/imgscraper/PAGEID/

