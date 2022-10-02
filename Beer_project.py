from textwrap import indent
import requests
import json

"""Amazon SDE Program | AMorales
   Final Project - Rate Craft Beer""" 

def welcome_message():
    """Prints the welcome message at the start of the program"""
    print("Track what beer you had at every Brewery you have Visited.")
    ## TODO: move the message about beer rating to the prompt that is asking for a beer rating.
    print("Search the brewery you have been to by name.\n Please rate the beer you had from 1 to 5.\n With a rating of 1 being your least favorite and rating of 5 being a most have again. ")

def prompt_legalAge():

    legalAge = int(input("You have to be 21 or older to access our application. How old are you? \n"))
    if (legalAge == 0):
        print("Please enter a valid input\n")
        return prompt_legalAge()
    elif legalAge <= 20:
        print("Access denied: You have to be older than 21 to access the application \n")
        raise Exception("Please come back when you're 21.")
    else: 
        return legalAge

def prompt_breweryname():

    breweryName = input("Enter the name of the Brewery? \n")
    
    if (len(breweryName) == 0):
        print("Please enter a valid input\n")
        return prompt_breweryname()
    else:
        return breweryName


def api_call(breweryName):
   
    
    API_ENDPOINT = f"https://api.openbrewerydb.org/breweries?by_name={breweryName}&per_page=5"
   
    response = requests.get(API_ENDPOINT)
    results = json.loads(response.content)
    return results

def get_correct_brewery_name(results):
    print("Did you mean?")
    i = 1
    for result in results:
        print(f"{i}: {result['name']}, {result['city']}, {result['state']}")
        i+=1
    selection = int(input("Please select the number of the brewery you want? \n"))
    ## TODO: review how this works
    selection_output = {"name": results[selection - 1]["name"], "city": results[selection - 1]["city"], "state": results[selection - 1]["state"]} 
    return selection_output


def what_type_of_beer_did_you_have():

    beer_type = input("What is the name of the beer you had? \n")
    if (len(beer_type) == 0):
        print("Please enter a valid input\n")
        return what_type_of_beer_did_you_have()
    else:
        return beer_type

def what_do_you_rate_this_beer():

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

def write_the_rating_to_file(beer_tracking, beer, rate):
    ## TODO: refactor this to store each beer tried in a list associated with each brewery
    beer_tracking["Beer"] = beer
    beer_tracking["Rate"] = rate

    with open("tracking.text", "a+") as outfile:
        json.dump( beer_tracking, outfile)

    with open('tracking.text') as openfile: 
        beerList = json.load(openfile)
        print("Brewery and Beer List = ", beerList)
    # with open('tracking.text', "r") as openfile:
    #     for beerObj in openfile:
    #         beer_output = json.load(beerObj.readlines())
    #         beer_tracking.extend(beer_output)
    #         print(beer_output)
    


    # with open("tracking.text", "a+") as outfile:
    #     json.dump( beer_tracking, outfile,)

    # with open('tracking.text') as openfile:
    #     # for beerObj in openfile:
    #         beer_output = json.load(openfile.read())
    #         beer_tracking.extend(beer_output)
    #         print(beer_output)
    

    # with open("tracking.json", "a+") as outfile:
    #     json.dump( beer_tracking, outfile,)

    # with open('tracking.json', 'r+') as openfile:
    #     beer_output = json.load(openfile)
    #     print(beer_output)
def enter_anotherBrewery():    

    more_beer = input("Do you want to enter another beer rating? yes/no \n")
    if more_beer not in ["yes", "no"]:
        print("Please enter a valid input\n")
        return enter_anotherBrewery()
    elif (more_beer == "yes"):
        return prompt_breweryname()
    else:    
        print("Thank you for visiting my application.")
    

def main():
    welcome_message()
    prompt_legalAge()
    breweryname = prompt_breweryname()
    results = api_call(breweryname)
    correct_brewery = get_correct_brewery_name(results)
    beer = what_type_of_beer_did_you_have()
    rate = what_do_you_rate_this_beer()
    write_the_rating_to_file(correct_brewery, beer, rate)
    enter_anotherBrewery()
      
if __name__=="__main__":

    main()
