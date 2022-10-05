import requests
import json
import os

"""Amazon SDE Program | AMorales
   Final Project - Rate Craft Beer""" 

file_path = "./tracking.json"
def load_data(file_path):
    """Loads the brewery from tracking.json"""

    with open(file_path, "r") as infile:
        return json.load(infile)

def welcome_message():
    """Prints the welcome message at the start of the program"""
    os.system("clear")
    print("="*70)
    print("Welcome to Mike's Craft Beer Tracker.")
    print("Log and rate what beer you had at every brewery you have visited.")
    print("="*70)

def prompt_legalAge():

    legalAge = int(input("You have to be 21 or older to access our application. How old are you? \n"))
    if (legalAge == 0):
        print("Please enter a valid input\n")
        return prompt_legalAge()
    elif legalAge <= 20:
        print("Access denied: You have to be older than 21 to access the application \n")
        exit()
    else: 
        return legalAge

def prompt_breweryname():
    """prompt user for the brewery. Validates if the user enter a valid input"""
    os.system("clear")
    breweryName = input("Enter the name of the Brewery you have visited: \n")
    
    if (len(breweryName) == 0):
        print("Invalid input. Please enter the name of the Brewery you have visited\n")
        return prompt_breweryname()
    else:
        return breweryName

def api_call(breweryName):
    """Once the user enters the name of a valid Brewery the Api gets the information from the Brewery."""
    #TODO Review lab 55 Define our "base" API
    #TODO: Possibly implement pagination to get more than 10 results
    API_ENDPOINT = f"https://api.openbrewerydb.org/breweries?by_name={breweryName}&per_page=10"
   
    response = requests.get(API_ENDPOINT)
    results = json.loads(response.content)
    return results

def get_correct_brewery_name(results):
    """
    Function collects the data acquired by the API and displays the correct name of the Brewery. 
    Since the user can type "silos" however the correct name is: 2 Silos Brewing Company.
    """
    print("Did you mean?")
    i = 1
    for result in results:
        print(f"{i}: {result['name']}, {result['city']}, {result['state']}")
        i+=1
    selection = int(input("Please select the number of the brewery you want? \n"))

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
            "ratings": [],
        }
    return brewery_data

def what_type_of_beer_did_you_have():
    """ This function ask the user the name of the beer they had at the brewery.""" 
    os.system("clear")
    beer_type = input("What is the name of the beer you had? \n")
    if (len(beer_type) == 0):
        print("Invalid Input. Please enter what is the name of the beer you had\n")
        return what_type_of_beer_did_you_have()
    else:
        return beer_type

def what_do_you_rate_this_beer():
    """
    How the user would rate his beer with a rating of 1 being your least favorite and rating of 5 being a most have again. 
    Had the user validation less than 0 and more than 6. However is the user typed 1.5 it broke the app. The try and except mitigated that.
    """
    os.system("clear")
    try:
        rate_beer = int(input("From 1 to 5 how would you rate the beer? \n"))
    except ValueError:
        print("Please enter a whole number from 1 to 5")
        return what_do_you_rate_this_beer()
    if rate_beer <= 0 or rate_beer >= 6:
        print("Please enter a whole number from 1 to 5\n")
        return what_do_you_rate_this_beer()
    else:
        return rate_beer

def add_ratings_to_brewery_data(brewery_data, brewery_add_data):
    repeat = "yes"

    while repeat == "yes":
        beer = what_type_of_beer_did_you_have()
        rate = what_do_you_rate_this_beer()
        brewery_data[brewery_add_data["id"]]["ratings"].append({"beer": beer, "rate":rate})
        repeat = input("Do you want to enter another beer? (yes/no) \n")
    return brewery_data

def write_the_rating_to_file(brewery_data):
    """Once the application has the brewery inf and user input (beer&rate) the data is saved in a text file in order to display the inf to the user."""
    with open(file_path, "w") as outfile:
        json.dump(brewery_data, outfile)
    
def rate_beer(brewery_data):
    breweryname = prompt_breweryname()
    results = api_call(breweryname)
    brewery_add_data = get_correct_brewery_name(results)
    brewery_data = add_brewery_to_brewery_data(brewery_data, brewery_add_data)
    brewery_data = add_ratings_to_brewery_data(brewery_data, brewery_add_data)
    write_the_rating_to_file(brewery_data)
    rate_again = input("do you want to rate beer at another brewery? (yes/no) \n")
    if rate_again == "yes":
        rate_beer(brewery_data)
    else:
        menu(brewery_data)

def display_ratings(brewery_data):
    os.system("clear")
    for brewery in brewery_data.values():
        print (f"Brewery name: {brewery['name']}, {brewery['city']}, {brewery['state']}")
        print("\tYou tried the following beers:")
        for rating in brewery["ratings"]:
            print(f"\t\tBeer name: {rating['beer']}, rating: {rating['rate']}")
        print("\n")
    input("Press enter to continue...")
    menu(brewery_data)

def menu(brewery_data):

    print("Choose the number of the action you would like to perform")
    print("1: Enter a new Brewery")
    print("2: Display all the beers and their ratings")
    choose = int(input("Enter the number:\n"))

    if choose == 1:
        rate_beer(brewery_data)
    if choose == 2:
        display_ratings(brewery_data)
        
    else:
        welcome_message()

def main():
    brewery_data = load_data(file_path)
    prompt_legalAge()   
    welcome_message()
    menu(brewery_data)
         
      
if __name__=="__main__":
    
    main()