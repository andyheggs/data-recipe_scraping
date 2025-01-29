# pylint: disable=missing-docstring, line-too-long, missing-timeout
import sys
import csv
import requests
from os import path, makedirs
from bs4 import BeautifulSoup

# This initial parsing block is unused and can be removed.
# soup = BeautifulSoup(open("pages/carrot.html"), "html.parser")
# for recipe in soup.find_all('p', class_='recipe-name'):
#     print(recipe.text)

#---------------------------------------------------2. Parse HTML------------------------------------------------------#
def parse(html):
    # Create BeautifulSoup object to parse HTML content
    soup = BeautifulSoup(html, "html.parser")
    # Initialize empty list to store parsed recipe data
    results = []
    # Iterate over all <div> elements with class of 'recipe' in soup object
    for article in soup.find_all('div', class_='recipe'):
        # Parse individual recipe data from article element using parse_recipe func.
        recipe_data = parse_recipe(article)
        # Append parsed recipe data to results list
        results.append(recipe_data)
    # Return list of parsed recipes
    return results

#----------------------------------------------1. Parse single recipe--------------------------------------------------#
def parse_recipe(article):
    # Extract recipe name by finding the <p> tag with class 'recipe-name' and remove any leading/trailing whitespace
    name = article.find('p', class_='recipe-name').text.strip()
    # Extract difficulty and preparation time similarly
    difficulty = article.find('p', class_='recipe-difficulty').text.strip()
    prep_time = article.find('p', class_='recipe-time').text.strip()
    # Return a dictionary containing extracted name, difficulty, and prep time of recipe
    return {
        'name': name,
        'difficulty': difficulty,
        'prep_time': prep_time
    }

#----------------------------------------------3. Write List-----------------------------------------------------------#
def write_csv(ingredient, recipes):
    # Ensure 'recipes' directory exists; create if not
    makedirs('recipes', exist_ok=True)
    # Define file path for CSV file based on given ingredient
    filepath = path.join('recipes', f'{ingredient}.csv')
    # Open CSV file for writing, with specified newline and encoding settings
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        # Initialize CSV DictWriter to write dictionaries to file.
        writer = csv.DictWriter(file, fieldnames=["name", "difficulty", "prep_time"])
        # Write header row to CSV file using defined fieldnames.
        writer.writeheader()
        # Iterate over each recipe in list of recipes and write as a row.
        for recipe in recipes:
            writer.writerow(recipe)

#-------------------------------------------------4. Scrape------------------------------------------------------------#
def scrape_from_internet(ingredient, start=1):
    # Construct URL for recipe search page using provided ingredient and page number
    url = f"https://recipes.lewagon.com/?search[query]={ingredient}&page={start}"
    # Send GET request to constructed URL and store response
    response = requests.get(url)
    # Raise error if GET request resulted in unsuccessful status code
    response.raise_for_status()  # Handle any HTTP errors
    # Return content of response as string (HTML page content)
    return response.text

#----------------------------------------------------------------------------------------------------------------------#

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file, encoding='utf-8')
    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)

#----------------------------------------------5. Update Main----------------------------------------------------------#

def main():
    # Check if script was called with argument for ingredient
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        # Initialize list to accumulate recipes from multiple pages
        all_recipes = []
        # Loop over first 3 pages to collect recipes
        for page in range(1, 4):
            # Scrape HTML content for current page of ingredient's recipes
            html = scrape_from_internet(ingredient, start=page)
            # Parse scraped HTML to extract recipes
            recipes = parse(html)
            # If recipes found, extend all_recipes list; else, terminate loop early
            if recipes:
                all_recipes.extend(recipes)
            else:
                break
        # Write collected recipes to CSV file named after ingredient
        write_csv(ingredient, all_recipes)
        # Inform user recipes were successfully written to CSV file
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        # If no ingredient provided, print usage instructions and exit
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)

if __name__ == '__main__':
    main()
