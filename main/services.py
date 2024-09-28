# recipes/services.py
import requests

def get_recipe_by_dish_name(dish_name):
    api_key = '2aa152d144034dcdac8d3d32a71a912d'
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'query': dish_name,
        'number': 5,  # Fetch up to 5 recipes
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['results']
