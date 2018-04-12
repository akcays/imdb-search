import json
import functools

movies = json.load(open('movies.json'))

def search_title(title, movies):

    """
    title (str): movie title
    movies (list): List of movie in Dictionary format
    returns a List of movie titles
    """

    result = []

    title = title.strip().lower()

    for movie in movies:

        movie_title = movie["title"].lower()

        if title in movie_title:

            result.append(movie["title"])

    return result

def search_director(director, movies):

    """
    director (str): movie director
    movies (list): List of movie in Dictionary format
    returns a List of movie titles
    """

    result = []

    director = director.strip().lower()

    for movie in movies:

        movie_director = movie["director"].lower()

        if director in movie_director:

            result.append(movie["title"])

    return result

def search_stars(star, movies):

    """
    star (str): movie star
    movies (list): List of movie in Dictionary format
    returns a List of movie titles
    """

    result = []

    star = star.strip().lower()

    for movie in movies:
        
        stars = [movie_star.lower() for movie_star in movie["stars"]]
        movie_stars = " ".join(stars)

        if star in movie_stars:

            result.append(movie["title"])

    return result

def search_movies(query, movies):

    """
    query (str): keywords to search in database
    movies (list): List of movie in Dictionary format
    returns a List of movie titles
    """

    result = []

    words = [word.lower().strip() for word in query.split(" ")]

    data = {}

    for word in words:

        data[word] = []

        data[word] += search_stars(word, movies)
        data[word] += search_director(word, movies)
        data[word] += search_title(word, movies)

        data[word] = set(data[word])

    result = functools.reduce(lambda x,y: x.intersection(y), data.values())

    return list(result)

def search(query):

    """
    query (str): keywords to search in database
    returns a List of movie titles
    """

    return search_movies(query, movies)


if __name__ == "__main__":

    print("")
    print('Searching for "Spielberg"')
    print(search("spielberg"))
    print("")
    print('Searching for "Hanks"')
    print(search("hanks"))
    print("")
    print('Searching for "Spielberg" and "Hanks"')
    print(search("spielberg hanks"))
