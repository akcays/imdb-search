from bs4 import BeautifulSoup
import json
import requests
import queue
import threading
import time

pages_urls = queue.Queue()
movies = queue.Queue()
output_data = queue.Queue()
pages_fail = queue.Queue()
movies_fail = queue.Queue()

main_url = "http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page={0}&ref_=adv_nxt"

# populate the first Queue
for i in range(1, 21):

    url_format = main_url.format(i)
    pages_urls.put(url_format)

class PageRunnable():
 
    def __call__(self):
 
        message = "\nThread {0} working hard"
 
        def process_data(url):
 
            try:
                url_get = requests.get(url)
                html_soup = BeautifulSoup(url_get.content, 'lxml')
 
            
                movie_list = html_soup.select('.lister-item')

                for movie in movie_list:
                    
                    div = movie.select('.col-title')[0]
                    span = div.select('span')[0]
                    a_tag = div.select('a')[0]

                    link = a_tag.get('href')
                    title = a_tag.text

                    movie_dict = dict()
                    movie_dict["title"] = title
                    movie_dict["url"] = "http://www.imdb.com" + link

                    movies.put(movie_dict)
                    
            except:

                pages_fail.put(url)
 
        while True:
 
            try:
 
                url = pages_urls.get(timeout=1)
 
            except:
 
                break
 
            print(message.format(id(self)))
 
            process_data(url)


class MovieRunnable():
 
    def __call__(self):
 
        message = "\nThread {0} working hard"
 
        def process_data(movie_dict):
 
            try:
                url_get = requests.get(movie_dict["url"])
                html_soup = BeautifulSoup(url_get.content, 'lxml')
                
                data = html_soup.select('.plot_summary')[0]

                # Getting the description

                summary = data.select('.summary_text')[0].text.strip()
                movie_dict["description"] = summary

                summary_items = data.select('.credit_summary_item')
                
                # Getting the Director

                director = summary_items[0].select('a > span')[0].text.strip()
                movie_dict["director"] = director

                stars_index = 1
                
                if len(summary_items) > 2:

                    # Getting the writers

                    writers = list()

                    spans = summary_items[1].findAll('span', {"itemprop": "name"})

                    for span in spans:
                    
                        writer = span.text.strip()
                        writers.append(writer)
                    
                    movie_dict["writers"] = writers

                    stars_index = 2

                else:

                    movie_dict["writers"] = []

                # Getting the stars

                stars = list()

                spans = summary_items[stars_index].findAll('span', {"itemprop": "name"})

                for span in spans:
                    
                    star = span.text.strip()
                    stars.append(star)
                    
                movie_dict["stars"] = stars
                print(movie_dict)

                output_data.put(movie_dict)
                    
            except:

                movies_fail.put(movie_dict)
 
        while True:
 
            try:
 
                movie_dict = movies.get(timeout=1)
 
            except:
 
                break
 
            print(message.format(id(self)))
 
            process_data(movie_dict)

tick = time.time()

# Threads

threads = []

# PageRunnable Pool

for i in range(4):
 
    new_thread = threading.Thread(target=PageRunnable())
    new_thread.start()
    threads.append(new_thread)
 
for thread in threads:
 
    thread.join()

# MovieRunnable Pool

for i in range(4):
 
    new_thread = threading.Thread(target=MovieRunnable())
    new_thread.start()
    threads.append(new_thread)
 
for thread in threads:
 
    thread.join()

tock = time.time()

print("---- {0} seconds ----".format(tock - tick))

def queue_to_list(q):
    """ Dump a Queue to a list """

    l = []

    while True:
        try:
            l.append(q.get(timeout=1))
        except:
            break
    return l

result = queue_to_list(output_data)
pages_failed = queue_to_list(pages_fail)
movies_failed = queue_to_list(movies_fail)

with open('movies.json', 'w') as outfile:

    json.dump(result, outfile, sort_keys=True, indent=4)
