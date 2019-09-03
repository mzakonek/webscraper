# webscraper

REST API for scrapping data (text and images) from websites.

# Installation
1. Clone this repository: git clone https://github.com/mzakonek/webscraper.git
2. cd into webscraper: cd webscraper
3. install requirements: pip install -r requirements.txt
4. run command: python manage.py makemigrations
5. run command: python manage.py migrate
6. download and install Redis, open terminal and run: redis-server
7. open new terminal window, activate our virtual environment and run: celery worker -A webscraper --loglevel=info


# curls
## Pages
create new url record in db

curl -d "url=<url page e.g. http://wyborcza.pl>" -X POST http://localhost:8000/api/pages/

check details about this url in db

curl -X GET http://localhost:8000/api/pages/ <pageid> /

## Text scraper
start process of scrapping text from url

curl -X POST http://localhost:8000/api/textscraper/?urlid=<pageid>

get data scrapped from page

curl -X GET http://localhost:8000/api/textscraper/<pageid>/

## Image scraper
start process of scrapping imgs from url

curl -X POST http://localhost:8000/api/imgscraper/?urlid=<pageid>

get imgs scrapped from page

curl -X GET http://localhost:8000/api/imgscraper/<pageid>/

