# pylint: disable=missing-docstring, line-too-long, missing-timeout
import sys
from os import path
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("pages/carrot.html"), "html.parser")

for recipe in soup.find_all('p', class_= 'recipe-name'):
    print(recipe.text)

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    pass  # YOUR CODE HERE

def parse_recipe(article):
    # Extract recipe name by finding the <p> tag with class 'recipe-name' and remove any leading/trailing whitespace
    name = article.find('p', class_='recipe-name').text.strip()

    # Extract recipe difficulty by finding the <p> tag with class 'recipe-difficulty' , remove any leading/trailing whitespace
    difficulty = article.find('p', class_='recipe-difficulty').text.strip()

    # Extract preparation time by finding <p> tag with class 'recipe-time' , remove any leading/trailing whitespace
    prep_time = article.find('p', class_='recipe-time').text.strip()

    # Return a dictionary containing extracted name, difficulty, and prep time of recipe
    return {
        'name': name,
        'difficulty': difficulty,
        'prep_time': prep_time
    }

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    pass  # YOUR CODE HERE

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    pass  # YOUR CODE HERE

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"

    if path.exists(file):
        return open(file, encoding='utf-8')

    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')

    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]

        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_file(ingredient))

        pass  # YOUR CODE HERE
        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
