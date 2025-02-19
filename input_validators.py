from colors_library import *


def if_input_empty(prompt):
    """ This function is used in add_movie() to check if the input is empty. """
    while True:
        user_input = input(prompt)
        if user_input == '':
            print(red_on_black('Field is empty'))
        else:
            return user_input


def input_float_or_int(prompt):
    """ This function is used in add_movie() to check if the entered rating is int or float. """
    while True:
        user_input = input(prompt)
        try:
            float(user_input)
            if not 0 < float(user_input) <= 10:
                raise Exception(red_on_black("Expected a number (1.0 - 10.0)"))
        except ValueError:
            print(red_on_black("Expected a number (0.0 - 10.0)"))
        except Exception as error:
            print(error)
        else:
            return float(user_input)


def input_year(prompt):
    """ This function is used in add_movie()
        Checks if the entered 'input_year' contains 4 digits.
    """
    while True:
        user_input = input(prompt)
        try:
            if not user_input.isdigit() or len(user_input) != 4:
                raise Exception(red_on_black("is not a valid year"))
        except Exception as error:
            print(error)
        else:
            return user_input


def input_yes_or_no(prompt):
    """ Prompts the user for YES or NO in sort_movies_by_years() """
    while True:
        input_user = input(prompt)
        input_user.lower()
        if input_user == "y":
            return True
        elif input_user == "n":
            return False
        else:
            print('Please enter "Y" or "N"')


def input_min_rating(prompt):
    """
        Prompts the user for a minimum rating and returns 0
        if the user doesn't enter an answer.
    """
    while True:
        user_input = input(prompt)
        if user_input == '':
            return 0
        try:
            float(user_input)
            if not 0 < float(user_input) <= 10:
                raise Exception(red_on_black("Expected a number (0.0 - 10.0)"))
        except ValueError:
            print(red_on_black("Expected a number (0.0 - 10.0)"))
        except Exception as error:
            print(error)
        else:
            return float(user_input)


def input_start_end_year(prompt):
    """
        This function is used in the function filter_movies
        Prompts the user for a year
    """
    while True:
        user_input = input(prompt)
        if user_input == '':
            return 0
        try:
            if not user_input.isdigit() or len(user_input) != 4:
                raise Exception(red_on_black("is not a valid year"))
        except Exception as error:
            print(error)
        else:
            return int(user_input)