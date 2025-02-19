""" colors module """

def red_on_black(string):
    return f"\033[1;31;40m{string}\033[0;0m"

def green_on_black(string):
    return f"\033[1;32;40m{string}\033[0;0m"

def yellow_on_black(string):
    return f"\033[1;33;40m{string}\033[0;0m"

def lightblue_on_black(string):
    return f"\033[1;34;40m{string}\033[0;0m"

def magenta_on_black(string):
    return f"\033[1;35;40m{string}\033[0;0m"

def black_on_red(string):
    return f"\033[1;30;41m{string}\033[0;0m"

def black_on_green(string):
    return f"\033[1;30;42m{string}\033[0;0m"

def black_on_yellow(string):
    return f"\033[1;30;43m{string}\033[0;0m"

def black_on_lightblue(string):
    return f"\033[1;30;44m{string}\033[0;0m"

def black_on_magenta(string):
    return f"\033[1;30;45m{string}\033[0;0m"

def main():
    pass

if __name__ == "__main__":
    main()
