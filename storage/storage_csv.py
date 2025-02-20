from storage.istorage import IStorage
import csv
from colors_library import *


class StorageCsv(IStorage):
    """
        This class allows the storage in a csv file
    """
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
        """
        Reads the data in a csv file and returns a dictionary
        """
        list_movies = {}
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as archivo_csv:
                reader = csv.reader(archivo_csv)
                next(reader)  # Skip header
                for row in reader:
                    title, rating, year, poster = row
                    list_movies[title] = {'rating': float(rating), 'year': int(year), 'poster': poster}
        except FileNotFoundError:
            print("File doesn't exist.")
        return list_movies


    def save_movies(self, movies_updated):
        """
            Gets all movies data from a dictionary "movies_updated" as an argument
            Saves the data to the movies.csv file.
        """
        with open(self.file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # writes heads
            writer.writerow(['title', 'rating', 'year', 'poster'])
            # writes data
            for key, values in movies_updated.items():
                writer.writerow([key, values['rating'], values['year'], values['poster']])


    def add_movie(self, title, year, rating, poster):
        """
            Gets title, rating and year from user
            Adds a movie to the dictionary “list_movies”.
            Updates the csv file with the save_movies() method.
        """
        list_movies = self.list_movies()
        list_movies[title] = {"rating": rating, "year": year, "poster": poster}
        self.save_movies(list_movies)
        print(green_on_black(f"Movie '{title}' successfully added"))


    def delete_movie(self, title):
        """
            Prompts the user for a title and checks if it exists in list_movies.
            If it finds the title, it deletes the movie from list_movies.
            Updates the csv file with the save_movies() method.
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
