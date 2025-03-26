import json

import requests



def get_recipes():
    """"Get all the recipes from the API."""
    request = requests.get("http://127.0.0.1:8000/api/v1/rgarcia/recetas/todas", timeout=10)
    if request.status_code == 200:
        print(request.content)
        return json.loads(request.content)
    return ''

def get_recipe(recipe_id : int):
    """"Get a recipe by its ID."""
    request = requests.get(f"http://127.0.0.1:8000/api/v1/rgarcia/recetas/receta?receta_id={recipe_id}", timeout=10)
    if request.status_code == 200:
        return json.loads(request.content)
    return ''

def post_recipe(data: dict):
    """Create a new recipe."""
    request = requests.post("http://127.0.0.1:8000/api/v1/rgarcia/recetas/alta", json=data, timeout=10)
    return request.json() if request.status_code == 200 else ''

def put_recipe(data: dict):
    """Update an existing recipe by its ID."""
    url = "http://127.0.0.1:8000/api/v1/rgarcia/recetas/modificar"
    request = requests.put(url, json=data, timeout=10)
    return request.json() if request.status_code == 200 else ''

def delete_recipe(recipe_id: int):
    """Delete a recipe by its ID."""
    request = requests.delete(f"http://127.0.0.1:8000/api/v1/rgarcia/recetas/eliminar?receta_id={recipe_id}", timeout=10)
    return request.json() if request.status_code == 200 else ''
