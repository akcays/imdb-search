# imdb-search
take-home exercise imdb scraper and search

## Installation Instructions

To run the project using a virtual environment, enter the commands below on your terminal.

```
git clone https://github.com/akcays/imdb-search

cd imdb-search

pip install virtualenv

python3 -m venv . 

source ./bin/activate

pip install BeautifulSoup4

pip install requests

pip install lxml
```

To run the singlethreaded version

`python3 web_scraper.py`

To run the multithreaded version

`python3 web_scraper_multithread.py`

At this point, a movies.json file should have been created with top 1000 movies, to run the api

`python3 movies_api.py`

## Stretch goals

* My first goal has been increasing the speed of fetching the top 1000 movies, for this I used `threading` module of Python to distribute the work among multiple workers/threads so that movies can load faster. 

* If I had more time, my other goal would be adding more metrics, such as 'rating', I'd return the results (movie titles) for a search by descending order of their ratings.
