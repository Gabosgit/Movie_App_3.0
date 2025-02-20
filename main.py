""" It generates an application using:
    movies.json file, StorageJson Class, MovieApp class
    sys is used to get an argument from the terminal
    NOTE: sys will be replaced with argparse in the future
"""
from movie_app import MovieApp
import sys
import csv
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv


def file_by_type(argv):
    """
    :param argv: Takes the file name
    :return: return a storage json or csv file
    Prints a msg if the extension is not supported
    """
    if argv[-4:] == 'json':
        return StorageJson(f'data/{argv}')
    elif argv[-3:] == 'csv':
        return StorageCsv(f'data/{argv}')
    else:
        print("The file type is not supported.")

def set_and_run_app(storage_file):
    storage = file_by_type(storage_file)
    movie_app = MovieApp(storage)
    movie_app.run()


def main():
    """
    Take the second argument from the terminal ( filename with its extension),
    after running python3 main.py.
    Creates a file if no file with this name exists.
    Select the appropriate storage file with respect to the file type.
    Create an instance of the storage class
    Create an instance of movie_app and run it.
    """
    storage_file = sys.argv[1]
    try:
        with open(f"data/{storage_file}", 'x', newline='', encoding='utf-8') as new_file:
            if storage_file[-4:] == 'json':
                new_file.write('{}')
            elif storage_file[-3:] == 'csv':
                writer = csv.writer(new_file)
                # writes heads
                writer.writerow(['title', 'rating', 'year', 'poster'])
            else:
                print("The file type is not supported.")
    except FileExistsError:
        set_and_run_app(storage_file)
    else:
        set_and_run_app(storage_file)

if __name__ == '__main__':
    main()
