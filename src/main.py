# Imports

import sys
import json
import pprint

import utils


# Main

def main():
        k = int(sys.argv[1])
        plot = sys.argv[2]
        release_year = sys.argv[3]
        if str.isdigit(release_year):
                release_year = int(release_year)
        genre = sys.argv[4]
        output = utils.get_movies(k, plot, release_year, genre)      
        pprint.pprint(output)
        with open("output.json", "w") as file:
                json.dump(output, file, indent=2) 

if __name__ == "__main__":
        main()


