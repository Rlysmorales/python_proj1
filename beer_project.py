#!/home/rlysmorales/projects/python_proj1/.venv/bin/python
"""Amazon SDE Program | AMorales
   Final Project - Rate Craft Beer"""

import os
import json
import requests


FILE_PATH = "./tracking.json"


def load_data(FILE_PATH):
    """Loads the brewery from tracking.json"""

    # If the file doesn't exit create it
    if not os.path.exists(FILE_PATH):
        # open the file ~./tracking.json and read
        with open(FILE_PATH, "w") as create_file:
            json.dump({}, create_file)

    with open(FILE_PATH, "r") as infile:
        # parses the JSON data, creates a Python dict with the data & returns
        return json.load(infile)


def welcome_message(clear=False):
    """Prints the welcome message at the start of the program"""
    if clear:
        os.system("clear")
    print("=" * 70)
    print("Welcome to Mike's Craft Beer Tracker.")
    print("Log and rate what beer you had at every brewery you have visited.")
    print("=" * 70)


def prompt_legal_age():
    """This will ask the user for their age
    in order to know if they can access the app.
    """
    welcome_message(clear=True)
    legal_age = input(
        "You have to be 21 or older to access our application. How old are you?\n"
    )

    try:
        if len(legal_age) == 0:
            # validates user input.
            print("Your input is too short. Please enter your age.\n")
            input("Press enter to continue...")
            return prompt_legal_age()
        if int(legal_age) <= 20:
            print(
                f"Access denied. Your age is {legal_age}. You must be 21 to access the Brewery App."
            )
            exit()
        return legal_age

    except ValueError:
        print("Please enter your age as a whole number.")
        input("Press enter to continue...")
        return prompt_legal_age()


def print_yes_no():
    """validates the user yes or no input"""
    print("Please enter yes or no.")
    input("Press enter to continue...")


def print_brewery(brewery_name):
    """
    Prints the name of the brewery the user picked and displays it in the CLI
    """
    os.system("clear")
    print(brewery_name)
    print("=" * 70)


def menu(brewery_data):
    """
    This is the menu that gives the user the option to:
    Enter a new Brewery or Display the information on the file
    """
    welcome_message(clear=True)
    print("Choose the number of the action you would like to perform")
    print("1: Enter a new Brewery")
    print("2: Display all the beers and their ratings")
    print("3: Erase all of the ratings")
    print("4: Exit")
    choose = input("Enter the number:\n")

    if choose == "1":
        os.system("clear")
        rate_beer(brewery_data)
    elif choose == "2":
        display_ratings(brewery_data)
    elif choose == "3":
        reset_tracking_file()
    elif choose == "4":
        exit()
    else:
        os.system("clear")
        print(f"'{choose}' is not one of the options")
        print("=" * 70)
        input("Press enter to continue...")
        menu(brewery_data)


def api_call(search_brewery_name):
    """
    Once the user enters the name of a valid Brewery the Api
    gets the information from the Brewery.
    """
    # Review lab 55 Define our "base" API. Lab 79: .json()
    # Possibly implement pagination to get more than 10 results

    api_endpoint = "https://api.openbrewerydb.org/breweries?"
    search = f"by_name={search_brewery_name}&per_page=10"
    # contains the data sent from the server in response to the GET request
    response = requests.get(api_endpoint + search)
    # used to access payload data in the JSON serialized format.
    return response.json()


def prompt_breweryname():
    """prompt user for the brewery. User input validation"""
    welcome_message(clear=True)

    search_brewery_name = input("Enter the name of the Brewery you have visited: \n")

    if len(search_brewery_name) == 0:
        print(
            "Your input is too short. Please enter the name of the Brewery you have visited:\n"
        )
        return prompt_breweryname()
    response = api_call(search_brewery_name)

    if len(response) == 0:
        print(f"No search results found for '{search_brewery_name}' please try again.")
        input("Press enter to continue...")
        return prompt_breweryname()
    return response


def get_correct_brewery_name(results):
    """
    Collects the data acquired by the API and displays the proper Brewery name.
    """
    welcome_message(clear=True)
    print("Pick a brewery by its number:")
    # The user can type "silos" but the proper name is: 2 Silos Brewing Company
    try:
        i = 1
        for result in results:
            print(f"{i}: {result['name']}, {result['city']}, {result['state']}")
            i += 1
        selection = int(input("Please select the number of the brewery you want:\n"))
    except ValueError:
        print(
            f"'{selection}' is not between 1 and {len(results)}. Please enter a whole number from 1 to {len(results)}"
        )
        input("Press enter to continue...")
        return get_correct_brewery_name(results)

    if selection not in range(1, len(results) + 1):
        print(
            f"'{selection}' is not between 1 and {len(results)}. Please enter a whole number from 1 to {len(results)}"
        )
        input("Press enter to continue...")
        return get_correct_brewery_name(results)
    brewery_add_data = {
        "id": results[selection - 1]["id"],
        "name": results[selection - 1]["name"],
        "city": results[selection - 1]["city"],
        "state": results[selection - 1]["state"],
    }
    return brewery_add_data


def add_brewery_to_brewery_data(brewery_data, brewery_add_data):
    """create a dictionary to store one brewery's data"""
    if brewery_add_data["id"] not in brewery_data:
        brewery_data[brewery_add_data["id"]] = {
            "name": brewery_add_data["name"],
            "city": brewery_add_data["city"],
            "state": brewery_add_data["state"],
            "ratings": [],  # Important: This is where we store our beer ratings later
        }
    return brewery_data


def what_type_of_beer_did_you_have(brewery_name):
    """Asks the user the name of the beer they had at the brewery."""
    print_brewery(brewery_name)
    beer_type = input("What is the name of the beer you had? \n")
    if len(beer_type) == 0:
        print(
            "Your input is too short. Please enter what is the name of the beer you had\n"
        )
        return what_type_of_beer_did_you_have(brewery_name)
    else:
        return beer_type


def what_do_you_rate_this_beer(brewery_name, beer_type):
    """
    How the user would rate his beer.
    """
    # If the user typed 1.5 it broke the app. The try/except mitigated that.
    try:
        print_brewery(brewery_name)
        print(
            "Rate your beer: With 1 being your least favorite and rating of 5 being a most have again."
        )
        print()
        rate_beer = int(
            input(f"Between 1 to 5 how would you rate the beer: {beer_type}? \n")
        )
    except ValueError:
        print("Please enter a whole number from 1 to 5")
        input("Press enter to continue...")
        return what_do_you_rate_this_beer(brewery_name, beer_type)
    if rate_beer <= 0 or rate_beer >= 6:
        print("Please enter a whole number from 1 to 5\n")
        input("Press enter to continue...")
        return what_do_you_rate_this_beer(brewery_name, beer_type)
    else:
        return rate_beer


def add_ratings_to_brewery_data(brewery_data, brewery_add_data):
    """Allows the user to input a beer name and a rating"""
    repeat = "yes"
    brewery_name = f"{brewery_add_data.get('name')}, {brewery_add_data.get('city')}, {brewery_add_data.get('state')}"

    while repeat == "yes":
        beer = what_type_of_beer_did_you_have(brewery_name)
        rate = what_do_you_rate_this_beer(brewery_name, beer)
        brewery_data[brewery_add_data["id"]][
            "ratings"
        ].append(  # this is where we add the beer ratings to the rating list attribute
            {"beer": beer, "rate": rate}
        )
        print_brewery(brewery_name)
        repeat = input("Do you want to enter another beer? (yes/no) \n")
        while repeat not in ["yes", "no"]:
            print_yes_no()
            repeat = input("Do you want to enter another beer? (yes/no) \n")
    return brewery_data


def write_the_rating_to_file(brewery_data):
    """
    Once the application has the brewery inf and user input (beer&rate)
    the data is saved in a text file in order to display the inf to the user.
    """
    # the “dump” function directly writes the dictionary to a file in JSON form
    # without needing to convert it into an actual JSON object.
    with open(FILE_PATH, "w") as outfile:
        # It takes 2 parameters:"brewery_data" name of a dictionary
        #  which should be converted to a JSON object
        # outfile is the pointer of the file opened
        json.dump(brewery_data, outfile)


def rate_beer(brewery_data):
    """
    Work flow of the application: user is prompt for a brewery name;
    The API is called; Confirms name of Brewery; Creates data structure;
    Writes data to the file.
    """
    results = prompt_breweryname()
    brewery_add_data = get_correct_brewery_name(results)
    brewery_data = add_brewery_to_brewery_data(brewery_data, brewery_add_data)
    brewery_data = add_ratings_to_brewery_data(brewery_data, brewery_add_data)
    write_the_rating_to_file(brewery_data)
    welcome_message(clear=True)
    rate_again = input("Do you want to rate a beer at another brewery? (yes/no) \n")
    while rate_again not in ["yes", "no"]:
        print_yes_no()
        welcome_message(clear=True)
        rate_again = input("Do you want to rate a beer at another brewery? (yes/no) \n")
    if rate_again == "yes":
        # runs the program again
        rate_beer(brewery_data)
    else:
        # clear and takes the user to the welcome page
        welcome_message(clear=True)
        menu(brewery_data)


def display_ratings(brewery_data):
    """If the user wish to see the data he has entered"""
    os.system("clear")
    for brewery in brewery_data.values():
        # This is the order/format the data will be display to the user.
        print(f"Brewery name: {brewery['name']}, {brewery['city']}, {brewery['state']}")
        print("\tYou tried the following beers:")
        for rating in brewery["ratings"]:
            print(f"\t\tBeer name: {rating['beer']}, rating: {rating['rate']}")
        print("\n")
    input("Press enter to continue...")
    menu(brewery_data)


def reset_tracking_file():
    """Erase the data in the tracking.json file"""
    welcome_message(clear=True)
    print("Are you sure you want to delete all of you entries from the system?")
    print("Once you delete the information you wont be able to recover the data.")
    print()
    confirm = input("I am sure I want to delete the file: (yes/no) \n")

    if confirm == "yes":
        write_the_rating_to_file({})
        brewery_data = {}
        menu(brewery_data)
    elif confirm == "no":
        menu(brewery_data)
    else:
        print_yes_no()
        reset_tracking_file()


def main():
    """This starts the program
    loads the file into memory;
    Depending on what the user pick in the menu function they will be sent
    to rate_beer() or display_rating()"""

    brewery_data = load_data(FILE_PATH)
    prompt_legal_age()
    menu(brewery_data)


if __name__ == "__main__":
    # Protects the program from running Without this guard it will run the program
    main()
