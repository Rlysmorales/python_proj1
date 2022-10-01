import requests
from requests.auth import HTTPBasicAuth
import lxml
from bs4 import BeautifulSoup
import json

"""Amazon SDE Program | AMorales
   Final Project - Recipes"""

print("Welcome to Mike Recipes ")

def prompt_user_with_choices():
    food_choices = ["pizza", "casserole", "bread", "soup", "tacos"]
    for i in range(0, 5):
        print (f"{i+1}: {food_choices[i]}")
    choice = input("Which one do you want? (1-5)\n")

    if choice in ["1", "2", "3", "4", "5"]:
        return food_choices[int(choice) - 1]
    else:
        print("That choice isn't in the list")
        return prompt_user_with_choices()


def prompt_user():

    choice = input("Which of the following meals would you like to cook? \n")
    if (len(choice) == 0):
        print("Please enter a valid input\n")
        return prompt_user()
    else:
        return choice

""" def choose_which_database_to_use():
    print("1: Spoontacular")
    print("2: The mealdb")

    api_db = {}
    input("Which food database do you want to use?") """

def api_call():
    API_ENDPOINT = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', '1')
    meal = prompt_user_with_choices()

    url = API_ENDPOINT + meal
    print(url)
    response = requests.get(url, headers=headers, auth=auth)

    soup = BeautifulSoup(response.content, features="lxml")
    print(soup.prettify())


""" Setup for Spoontacular 
    API_ENDPOINT = "https://api.spoonacular.com/recipes/complexSearch?query="
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth('apikey', '3c5b363208bc4aad9ea4159fd9f170bb')
    meal = prompt_user_with_choices()

    url = API_ENDPOINT + meal
    response = requests.get(url, headers=headers) """

    

api_call()
