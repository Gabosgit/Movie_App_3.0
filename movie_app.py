from input_validators import *
import statistics
import random
from rapidfuzz import fuzz
import os
from dotenv import load_dotenv
import requests

#loads variables from the .env file into the environment
load_dotenv()

# os.getenv() to access the environment variables loaded from the .env file
API_KEY = os.getenv('API_KEY')


def fetch_data(movie_title):
    """ Receives a 'movie_title' from the user as an argument.
        Gets the movie information from the API by request GET.
        If the response is 'OK' returns the movie infos as json data,
        if not, prints an error in the terminal """
    API_URL = f'https://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        json_data = response.json()
        return json_data
    else:
        print("Error:", response.status_code, response.text)


class MovieApp:
    """ This class allows to create an interface to manipulate movie data.
        Allows storage in different file types like json and csv.
    """
    def __init__(self, storage):
        self._storage = storage


    def _command_list_movies(self):
        """
            Prints the list of movies by iterating over the keys "title"
            and obtaining values "year" and "rating
        """
        list_movies = self._storage.list_movies()
        number_of_movies = len(list_movies)
        if number_of_movies == 0:
            print("Not enough movies.\nPlease add movies by choosing the option '2. Add movie'")
        else:
            print(f"\n{black_on_yellow(f' *** {number_of_movies} MOVIES IN TOTAL *** ')}")
            for title in list_movies.keys():
                rating = list_movies[title]['rating']
                year = list_movies[title]['year']
                print(f"{title} ({year}): {yellow_on_black(f' {rating} ')}")


    def _command_add(self):
        """ Takes an input title from the user.
            Checks if the title exists in the API
            Checks the connection with the API
            Passes the movie data to the class method add_movie()
        """
        title = if_input_empty(f"\n{black_on_yellow(' Enter new movie name: ')}")
        try:
            data_movie = fetch_data(title)
        except Exception:
            print(
                f'Connection to the API is not possible.\nCheck internet connection or other possible API connection problems.')
        else:
            try:
                title = data_movie['Title']
            except KeyError:
                print(f"The movie with the title ‘{title}’ is not found.")
            else:
                year = data_movie['Year']
                rating = float(data_movie['Ratings'][0]['Value'][:-3])
                poster_url = data_movie['Poster']
                self._storage.add_movie(title, year, rating, poster_url)


    def _command_delete(self):
        """
            Takes a movie title from the user
            Checks if the title exists in the movies list to delete it.
        """
        input_movie_to_delete = input(f"\n{black_on_yellow('Enter movie name to delete:')}")
        list_movies = self._storage.list_movies()
        if input_movie_to_delete in list_movies.keys():
            self._storage.delete_movie(input_movie_to_delete)
            print(green_on_black(f"Movie '{input_movie_to_delete}' successfully deleted"))
        else:
            print(red_on_black(f"Movie '{input_movie_to_delete}' doesn't exist!"))


    def _command_update(self):
        """
            Prompts the user for a title and a rating to update.
            If the movie exists in the movies list, it updates the movie's rating.
            Updates the storage file with the save_movies() method.
        """
        list_movies = self._storage.list_movies()
        input_movie_to_update = input(f"\n{black_on_yellow('Enter movie name to update:')}")
        if input_movie_to_update in list_movies.keys():
            input_new_movie_rating = float(input_float_or_int("Enter new movie rating (1-10): "))
            self._storage.update_movie(input_movie_to_update, input_new_movie_rating)
            print(green_on_black(f"Movie '{input_movie_to_update}' successfully updated"))
        else:
            print(red_on_black(f"Movie '{input_movie_to_update}' doesn't exist!"))


    def calc_average(self, movies_dictionary):
        """ Calculates the average of the ratings of a list of ratings. """
        list_movies = self._storage.list_movies()
        number_of_movies = len(movies_dictionary)
        if number_of_movies == 0:
            print("Not enough movies.\nPlease add movies by choosing the option '2. Add movie'")
        else:
            sum_ratings = 0
            for title in list_movies.keys():
                rating = list_movies[title]['rating']
                sum_ratings = sum_ratings + rating
            average_ratings = sum_ratings / number_of_movies
            return average_ratings


    def calc_median(self, movies_dictionary):
        """
            Calculates the median of the list of ratings.
            Uses the library statistics (median).
        """
        list_movies = self._storage.list_movies()
        list_of_ratings = []
        for title in movies_dictionary.keys():
            rating = list_movies[title]['rating']
            list_of_ratings.append(rating)
        rating_median = statistics.median(list_of_ratings)
        return rating_median


    def get_best_and_worst_movie(self, movies_dictionary):
        """
            Returns lists of the best and worst rated movies
            and their respective ratings.
        """
        list_movies = self._storage.list_movies()
        max_rating = 0
        min_rating = 10
        list_best_movies = []
        list_worse_movies = []
        for title in movies_dictionary.keys():  # get max and min rating
            rating = list_movies[title]['rating']
            if rating > max_rating:
                max_rating = rating
            elif rating < min_rating:
                min_rating = rating
        for title in movies_dictionary.keys():  # get list of respective movies
            rating = list_movies[title]['rating']
            if rating == max_rating:
                list_best_movies.append(title)
            if rating == min_rating:
                list_worse_movies.append(title)

        return list_best_movies, max_rating, list_worse_movies, min_rating


    def _command_movie_stats(self):
        """
            Prints the best and worst movie(s) returned by get_best_and_worst_movie()
            Prints the average and median returned by the calc_average() and calc_median()
        """
        list_movies = self._storage.list_movies()
        number_of_movies = len(list_movies)
        if number_of_movies == 0:
            print("Not enough movies.\nPlease add movies by choosing the option '2. Add movie'")
        else:
            print(f"\n{black_on_yellow(' *** STATS *** ')}\n")
            average = self.calc_average(list_movies)
            median = self.calc_median(list_movies)

            list_best_movies = self.get_best_and_worst_movie(list_movies)[0]
            max_rating = self.get_best_and_worst_movie(list_movies)[1]
            list_worst_movie = self.get_best_and_worst_movie(list_movies)[2]
            min_rating = self.get_best_and_worst_movie(list_movies)[3]
            print(lightblue_on_black(" Average rating: "), black_on_lightblue(f" {average:.2f} "), "\n")
            print(green_on_black(" Median rating: "), black_on_green(f" {median:.2f} "), "\n")
            for best_movie in list_best_movies:
                print(yellow_on_black(" Best movie: "), f" {best_movie}", black_on_yellow(f" {max_rating} "), "\n")
            for worst_movie in list_worst_movie:
                print(red_on_black(" Worst movie: "), f" {worst_movie}", black_on_red(f" {min_rating} "), "\n")


    def _command_random_movie(self):
        """
            Uses the “random” library
            Chooses a number in the range of the length of the movie list
            Prints the movie pointed at the index of this number.
        """
        list_movies = self._storage.list_movies()
        number_of_movies = len(list_movies)
        if number_of_movies == 0:
            print("Not enough movies.\nPlease add movies by choosing the option '2. Add movie'")
        else:
            if number_of_movies == 1:
                random_num = 0
            else:
                random_num = random.randrange(1, number_of_movies)
            # generate a list with the movie titles (KEYS of dict_movies)
            selected_random_movie = list(list_movies)[random_num]
            random_movie_rating = list_movies[selected_random_movie]['rating']
            random_movie_year = list_movies[selected_random_movie]['year']
            print(f"\n{black_on_yellow(' YOUR MOVIE FOR TONIGHT ')}")
            print(f"{selected_random_movie} ({random_movie_year}), it's rated",
                  lightblue_on_black(f" {random_movie_rating} "))


    def _command_search_movie(self):
        """
            Gets a string (title) from the user and iterates the movie dictionary
            checking if it contains this string.
            If the string is found, it prints the movie title.
            In addition, it uses the "rapidfuzz library" to search for alternative movies.
        """
        list_movies = self._storage.list_movies()
        input_movie_to_search = input(f"\n{black_on_yellow('Enter a part of the movie name:')}")
        input_lowercase = input_movie_to_search.lower()
        dic_string_found = {}
        dic_others_found = {}
        for title in list_movies.keys():
            rating = list_movies[title]['rating']
            year = list_movies[title]['year']
            movie_lowercase = title.lower()
            if input_lowercase in movie_lowercase:
                dic_string_found[title] = {'rating': rating, 'year': year}
            else:
                fuzz_ratio = fuzz.ratio(input_lowercase, movie_lowercase)
                # print(f"simple ratio: {fuzz_ratio}")
                fuzz_token_sort_ratio = fuzz.token_sort_ratio(input_lowercase, movie_lowercase)
                # print(f"fuzz_token_sort_ratio: {fuzz_token_sort_ratio}")
                fuzz_partial_ratio = fuzz.partial_ratio(input_lowercase, movie_lowercase)
                # print(f"fuzz_partial_ratio: {fuzz_partial_ratio}")
                if fuzz_ratio >= 60:
                    dic_others_found[title] = {'rating': rating, 'year': year}
                    # print(f"ratio: {fuzz_ratio}: {title}")
                elif fuzz_token_sort_ratio >= 60:
                    dic_others_found[title] = {'rating': rating, 'year': year}
                    # print(f"fuzz_token_sort_ratio: {fuzz_token_sort_ratio}: {title}")
                elif fuzz_partial_ratio >= 90:
                    dic_others_found[title] = {'rating': rating, 'year': year}
                    # print(f"fuzz_partial_ratio: {fuzz_partial_ratio}: {title}")

        print(f"\n{black_on_green(' FOUND MOVIE(S) ')}")
        if not dic_string_found:
            print(red_on_black(f" The movie '{input_movie_to_search}' was not found."))
        else:
            for movie in dic_string_found:
                rating = dic_string_found[movie]['rating']
                year = dic_string_found[movie]['year']
                print(f"{movie} ({year}), {green_on_black(f' {rating} ')}")

        print(f"\n{black_on_lightblue(' OTHER FOUND MOVIE(S) ')}")
        if not dic_others_found:
            print(red_on_black(" No movie was found."))
        else:
            for movie in dic_others_found:
                rating = dic_others_found[movie]['rating']
                year = dic_others_found[movie]['year']
                print(f"{movie} ({year}), {lightblue_on_black(f' {rating} ')}")


    def _get_rating(self, title):
        """ Function used as KEY to sort movies in the sort_movies_by_rating() """
        list_movies = self._storage.list_movies()
        rating = float(list_movies[title]['rating'])
        return rating


    def _command_sort_movies_by_rating(self):
        """
            Sorts the movies by rating and iterates
            the resulting list to print the sorted movies.
        """
        list_movies = self._storage.list_movies()
        sorted_by_rating_list = sorted(list_movies, key=self._get_rating, reverse=True)
        print("\n" + black_on_magenta(" *** MOVIES SORTED BY RATING *** "))
        for title in sorted_by_rating_list:
            year = list_movies[title]['year']
            rating = list_movies[title]['rating']
            print(f"{title} ({year}): " + magenta_on_black(f' {rating} '))


    def _get_year(self, title):
        """
            Function used as KEY to sort the movies
            in the sort_movies_by_years() method. """
        list_movies = self._storage.list_movies()
        year = int(list_movies[title]['year'])
        return year


    def _command_sort_movies_by_years(self):
        """
            Sorts the movies by year and iterates the resulting list
            to print the sorted movies.
        """
        list_movies = self._storage.list_movies()
        latest_first = input_yes_or_no(green_on_black(" Do you want the latest movies first? (Y/N) "))
        sortd_by_year_list = sorted(list_movies, key=self._get_year, reverse=latest_first)
        print("\n" + black_on_green(" *** MOVIES SORTED BY YEAR *** "))
        for title in sortd_by_year_list:
            year = list_movies[title]['year']
            rating = list_movies[title]['rating']
            print(f"{title} " + green_on_black(f"({year})") + f": {rating}")


    def _command_filter_movies(self):
        """
            Gets 'min_rating' from input_min_rating() in input_validations.py,
            Gets 'start_year' and 'end_year' from input_start_end_year() in input_validations.py.
            Deletes the movies in a "copy_dict_movies" using these criteria
            Prints the result
        """
        list_movies = self._storage.list_movies()
        min_rating = input_min_rating(f"Enter {red_on_black(' minimum rating ')} (leave blank for no minimum rating): ")
        start_year = input_start_end_year(f"Enter {green_on_black(' start year ')} (leave blank for no start year): ")
        end_year = input_start_end_year(f"Enter {lightblue_on_black(' end year ')} (leave blank for no end year): ")
        if end_year == 0:
            end_year = float('inf')
        copy_dict_movies = list_movies.copy()
        for title in list_movies.keys():
            rating = float(copy_dict_movies[title]['rating'])
            year = int(copy_dict_movies[title]['year'])
            if rating < min_rating or year < start_year or year > end_year:
                del copy_dict_movies[title]
        print(f"\n{black_on_red(' *** FILTERED MOVIES *** ')}")
        if len(copy_dict_movies) == 0:
            print("No movies have been found with the given criteria.")
        for title in copy_dict_movies:
            rating = copy_dict_movies[title]['rating']
            year = copy_dict_movies[title]['year']
            print(f"{title} ({year}): {rating}")


    def load_html_template(self, file_path):
        """ Loads the html template file """
        with open(file_path, "r") as html_file:
            text_data = html_file.read()
            return text_data


    def serialize_one_movie(self, data_movie):
        """ Handles a single movie serialization"""
        title = data_movie[0]
        year = data_movie[1]['year']
        poster_url = data_movie[1]['poster']

        output_line = ''  # define an empty string
        # # append information to each string
        output_line += '\n'
        output_line += '\t\t\t<div class="col">\n'
        output_line += f'\t\t\t\t<div class="poster"><img src="{poster_url}"></div>\n'
        output_line += f'\t\t\t\t<div class="title">{title}</div>\n'
        output_line += f'\t\t\t\t<div class="year">{year}</div>\n'
        output_line += '\t\t\t</div>\n'
        return output_line


    def serialize_all_movies(self):
        """
            Iterates the serialization of all movies using serialize_one_movie()
            Returns the html code (output) to add it in the html file with write_new_html().
        """
        list_movies = self._storage.list_movies()
        output = ''
        for movie in list_movies.items():
            output += self.serialize_one_movie(movie)
        return output


    def write_new_html(self, file_path):
        """
            Writes a html file replacing __TEMPLATE_MOVIE_GRID__
            with the html code returned from serialize_all_movies()
        """
        html_data = self.serialize_all_movies()
        template_html = self.load_html_template('_static/index_template.html')
        new_html_template = template_html.replace('__TEMPLATE_MOVIE_GRID__', html_data)
        #new_html_template = template_html.replace('__TEMPLATE_TITLE__', 'MOVIE APP 3.0')
        with open(file_path, "w") as new_html:
            new_html.write(new_html_template)
        print("An 'index.html' file was generated with the movies data.")


    def _command_generate_website(self):
        self.write_new_html('index.html')


    def run(self):
        """ Shows the "menu_to_print" in terminal
            Prompts the user to choose one option of the menu validates the input.
            Dispatches the methods with respect to the input chosen by the user.
            Calls a function pointed to in the dictionary "options_menu".
            0 exits the application.
            Invalid option raises an exception.  """
        # Print menu
        menu_to_print = (
            f"{black_on_yellow('  *** My Movies Database ***   ')} \n"
            f"\n {black_on_yellow(' MENU ')} \n "
            f" 0. Exit \n "
            f" 1. List movies \n "
            f" 2. Add movie \n "
            f" 3. Delete movie \n "
            f" 4. Update movie \n "
            f" 5. Stats \n "
            f" 6. Random movie \n "
            f" 7. Search movie \n "
            f" 8. Movies sorted by rating \n "
            f" 9. Movies sorted by year \n "
            f"10. Filter movies \n "
            f"11. Generate website")

        # Get use command
        options_menu = {
            '1': self._command_list_movies,
            '2': self._command_add,
            '3': self._command_delete,
            '4': self._command_update,
            '5': self._command_movie_stats,
            '6': self._command_random_movie,
            '7': self._command_search_movie,
            '8': self._command_sort_movies_by_rating,
            '9': self._command_sort_movies_by_years,
            '10': self._command_filter_movies,
            '11': self._command_generate_website
        }
      # Execute command
        while True:
            print(menu_to_print)
            input_menu_option = input(f"{lightblue_on_black(' Choose an option (1-11) and press ENTER: ')}\n")
            if input_menu_option == '0':  # 0 exit the app
                print("\n", yellow_on_black(" Bye Bye! "))
                break
            try:
                if input_menu_option not in options_menu:  # Invalid input raises exception
                    raise Exception(red_on_black(f" '{input_menu_option}' is not a valid option."))
            except Exception as error:
                print(error)
            else:
                options_menu[input_menu_option]()  # Valid input calls a function
            input(f"\n{lightblue_on_black(' press ENTER to continue ')}\n")
