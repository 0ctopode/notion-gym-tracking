from fetch import *
from pprint import pprint

import configparser

def main():
    rows, cols = process_database(retrieve_database())
    pprint(rows)
    pprint(cols)
    

if __name__ == "__main__":
    main()