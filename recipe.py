# pylint: disable=missing-docstring, line-too-long
import sys
import csv
from os import path, makedirs
import requests
from bs4 import BeautifulSoup

#----------------------------------------------------------------------------------------------------------------------#

def parse(html):
    """Parse the HTML of the given page and return a list of recipe dictionaries."""

    # Create a BeautifulSoup object for parsing the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Initialize an empty list to store parsed recipe data
    results = []

    # Each recipe is in <div class="recipe">
    for article in soup.find_all('div', class_='recipe'):

        # Parse each recipe and store its data
        recipe_data = parse_recipe(article)

        # Add parsed recipe data to results list
        results.append(recipe_data)

    # Return the list of parsed recipes
    return results

#----------------------------------------------------------------------------------------------------------------------#

def parse_recipe(article):
    """
    Parse an individual recipe <div> and return a dict with:
      - name (from p.recipe-name)
      - difficulty (from span.recipe-difficulty)
      - prep_time (from span.recipe-cooktime)
    """
    # Extract recipe name, difficulty, and preparation time from the HTML article
    name_element = article.find('p', class_='recipe-name')
    difficulty_element = article.find('span', class_='recipe-difficulty')
    prep_time_element = article.find('span', class_='recipe-cooktime')

    # Get text from the HTML elements, with 'Unknown' as default if element not found
    name = name_element.text.strip() if name_element else 'Unknown'
    difficulty = difficulty_element.text.strip() if difficulty_element else 'Unknown'
    prep_time = prep_time_element.text.strip() if prep_time_element else 'Unknown'

    # Return a dictionary containing the recipe's name, difficulty, and prep time
    return {
        'name': name,
        'difficulty': difficulty,
        'prep_time': prep_time
    }

#----------------------------------------------------------------------------------------------------------------------#

def write_csv(ingredient, recipes):
    """
    Write a list of recipe dictionaries to recipes/<ingredient>.csv
    Creates the 'recipes' folder if it does not exist.
    """
    # Create 'recipes' directory if it doesn't exist
    makedirs('recipes', exist_ok=True)

    # Filepath for the CSV file
    filepath = path.join('recipes', f'{ingredient}.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "difficulty", "prep_time"])

        # Write the CSV header
        writer.writeheader()
        for recipe in recipes:

            # Write each recipe dictionary as a row in the CSV
            writer.writerow(recipe)
#----------------------------------------------------------------------------------------------------------------------#


def scrape_from_internet(ingredient, start=1):
    """
    Retrieve HTML for the given ingredient & page from recipes.lewagon.com.
    The `start` param is used to load pages 1..3.
    """
    # URL with query parameters for the ingredient and page number
    url = f"https://recipes.lewagon.com/?search[query]={ingredient}&search[start]={start}"

    # Make a GET request to fetch the HTML
    response = requests.get(url, timeout=10)

    # Return the response's HTML content
    return response.text

#----------------------------------------------------------------------------------------------------------------------#

def main():
    """Scrape up to 3 pages of recipes for a given ingredient and store them in CSV."""

    # Check if the ingredient argument is provided
    if len(sys.argv) <= 1:

        # Print usage message if not provided
        print('Usage: python recipe.py INGREDIENT')

        # Exit the program
        sys.exit(0)

     # Get the ingredient from command-line arguments
    ingredient = sys.argv[1]

    # Initialize list to collect all recipes
    all_recipes = []

    # Loop over pages 1..3, collecting all recipes
    for page in range(1, 4):

        # Scrape the HTML content of the page
        html = scrape_from_internet(ingredient, start=page)

        # Parse the HTML to extract recipes
        recipes = parse(html)
        if recipes:

            # Add recipes to the cumulative list
            all_recipes.extend(recipes)
        else:
            # If no recipes on this page, stop scraping
            # Exit the loop if no recipes are found on a page
            break

    # Write all collected recipes to a CSV file
    write_csv(ingredient, all_recipes)

    # Print confirmation message
    print(f"Wrote recipes to recipes/{ingredient}.csv")
if __name__ == '__main__':
    main()
