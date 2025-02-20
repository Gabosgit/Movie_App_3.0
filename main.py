""" It generates an application using:
    movies.json file, StorageJson Class, MovieApp class
    sys is used to get an argument from the terminal
    NOTE: sys will be replaced with argparse in the future
"""
import sys
import csv
from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from colors_library import magenta_on_black


def file_by_type(argv):
    """
    :param argv: Takes the file name and type
    Select the appropriate storage file with respect to the file type.
    :return: return an instance of storage class for json or csv file
    Prints a msg if the extension is not supported
    """
    if argv[-4:] == 'json':
        return StorageJson(f'data/{argv}')
    elif argv[-3:] == 'csv':
        return StorageCsv(f'data/{argv}')
    else:
        print("The file type is not supported.")

def set_and_run_app(storage_file):
    """
    :param storage_file: Takes the filename and extension given by the user
    Create an instance of the storage class
    Create an instance of movie_app and run it.
    """
    storage = file_by_type(storage_file)
    movie_app = MovieApp(storage)
    movie_app.run()


def main():
    """
    Take the second argument from the terminal ( filename with its extension),
    after running python3 main.py.
    Creates a file if no file with this name exists.
    """
    storage_file = sys.argv[1]
    try:
        if storage_file[-4:] == 'json':
            with open(f"data/{storage_file}", 'x', newline='', encoding='utf-8') as new_file:
                new_file.write('{}')
        elif storage_file[-3:] == 'csv':
            with open(f"data/{storage_file}", 'x', newline='', encoding='utf-8') as new_file:
                writer = csv.writer(new_file)
                # writes heads
                writer.writerow(['title', 'rating', 'year', 'poster'])
        else:
            print(magenta_on_black("\nThe file type is not supported.\n"
                  "Please enter a file name with json or csv extension.\n"))
            return
    except FileExistsError:
        set_and_run_app(storage_file)
    else:
        set_and_run_app(storage_file)

if __name__ == '__main__':
    main()
