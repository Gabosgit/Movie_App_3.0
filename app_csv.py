"""
Creates a csv fila from a json file
"""
import csv
import json


def list_movies():
    """ Reads the data in a json file and returns a dictionary """
    with open('../data/movies.json', 'r') as data_file:
        data_json = data_file.read()
        data = json.loads(data_json)
    return data

dict_movies = list_movies()
print(dict_movies)


def save_movies(movies_updated):
    """
        Gets all movies data from a dictionary "movies_updated" as an argument
        Saves the data to the movies.csv file.
    """
    with open('../data/movies.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # writes heads
        writer.writerow(['title', 'rating', 'year', 'poster'])
        # writes data
        for key, values in movies_updated.items():
            writer.writerow([key, values['rating'], values['year'], values['poster']])

save_movies(dict_movies)