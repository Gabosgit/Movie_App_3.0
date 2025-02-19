from storage.istorage import IStorage
import json
from colors_library import *


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
        """ Reads the data in a json file and returns a dictionary """
        with open(self.file_path, 'r') as data_file:
            data_json = data_file.read()
            data = json.loads(data_json)
        return data


    def save_movies(self, movies_updated):
        """
            Gets all movies data from a dictionary "movies_updated" as an argument
            Saves the data to the movies.json file.
        """
        with open(self.file_path, 'w') as json_file:
            new_data = json.dumps(movies_updated)
            json_file.write(new_data)


    def add_movie(self, title, year, rating, poster):
        """
            Gets title, rating and year from user
            Adds a movie to the dictionary “list_movies”.
            Updates the json file with the save_movies() method.
        """
        list_movies = self.list_movies()
        list_movies[title] = {"rating": rating, "year": year, "poster": poster}
        self.save_movies(list_movies)
        print(green_on_black(f"Movie '{title}' successfully added"))


    def delete_movie(self, title):
        """
            Prompts the user for a title and checks if it exists in list_movies.
            If it finds the title, it deletes the movie from list_movies.
            Updates the json file with the save_movies() method.
        """
        list_movies = self.list_movies()
        del list_movies[title]
        self.save_movies(list_movies)


    def update_movie(self, title, rating):
        """
            Takes a title and a value to update the rating
        """
        list_movies = self.list_movies()
        list_movies[title]["rating"] = rating
        self.save_movies(list_movies)
