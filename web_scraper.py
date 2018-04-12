from bs4 import BeautifulSoup
import json
import requests

main_url = "http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page={0}&ref_=adv_nxt"
movies = []

movie_count = 0

for i in range(1, 21):

    print("Processing page: {0} \n".format(i))
    url_get = requests.get(main_url.format(i))
    html_soup = BeautifulSoup(url_get.content, 'html5lib')

    movie_list = html_soup.select('.lister-item')

    for movie in movie_list:

        movie_count += 1
        
        div = movie.select('.col-title')[0]
        span = div.select('span')[0]
        a_tag = div.select('a')[0]

        link = a_tag.get('href')
        title = a_tag.text

        movie_dict = dict()
        movie_dict["title"] = title
        movie_dict["url"] = "http://www.imdb.com" + link
        movie_dict["rank"] = movie_count
        
        print("")
        print(u"Processing {0}: {1}".format(movie_count, movie_dict["title"]))
        
        url_get = requests.get(movie_dict["url"])
        html_soup = BeautifulSoup(url_get.content, 'html5lib')
        
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

            writers = []

            spans = summary_items[1].findAll('span', {"itemprop": "name"})

            for span in spans:
            
                writer = span.text.strip()
                writers.append(writer)
            
            movie_dict["writers"] = writers

            stars_index = 2

        else:

            movie_dict["writers"] = []

        # Getting the stars

        stars = []

        spans = summary_items[stars_index].findAll('span', {"itemprop": "name"})

        for span in spans:
            
            star = span.text.strip()
            stars.append(star)
            
        movie_dict["stars"] = stars

        print("")
        print(movie_dict)
        
        movies.append(movie_dict)
    
result = []

with open('movies.json', 'w') as outfile:

    json.dump(movies, outfile, indent=4)
