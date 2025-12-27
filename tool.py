#1 High protein food
def protein(min_protein:int, max_protein:int, page:int):
  import requests
  #this tool give the list of high protein dishes by taking input minimum and maximum protein range with page number.
  url = "https://api.foodoscope.com/recipe2-api/protein/protein-range"

  params = {
    'min': min_protein,
    'max': max_protein,
    'page': page,
    'limit': 10
}
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
}

  response = requests.get(url, params=params, headers=headers)
  return response.json()



#2 High energy food
def Energy(min_energy:int, max_energy:int, page:int):
    import requests
    #this tool give the list of high energy dishes by taking input minimum and maximum energy range with page number.
    url = "https://api.foodoscope.com/recipe2-api/byenergy/energy"

    # Query parameters can also be passed as a dictionary to the params argument
    params = {
  'minEnergy': min_energy,
  'maxEnergy': max_energy,
  'page': page,
  'limit': 10
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
    }

    response = requests.get(
    url,
    params=params,
    headers=headers
    )

    return response.json()



#3 High Carbs food
def Carbs(min_carbs:int, max_carbs:int):
  #this tool give the list of high carbs dishes by taking input minimum and maximum carbs range.
    import requests
    url = "https://api.foodoscope.com/recipe2-api/recipe-carbo/recipes-by-carbs"

    # Query parameters can also be passed as a dictionary to the params argument
    params = {
  'minCarbs': min_carbs,
  'maxCarbs': max_carbs,
  'limit': 10
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
}

    response = requests.get(
    url,
    params=params,
    headers=headers
)

    return response.json()



#4 Diet by region
def diet_by_region(Region:str, diet:str):
  #this tool give the list of dishes according to region and diet type by taking input of region name and diet catagory.
    import requests
    url = "https://api.foodoscope.com/recipe2-api/recipe/region-diet/region-diet"

    # Query parameters can also be passed as a dictionary to the params argument
    params = {
  'region': Region,
  'diet': diet,
  'limit': 10
  }

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
  }

    response = requests.get(
    url,
    params=params,
    headers=headers
  )

    return response.json()


#5 Recipe by including and excluding ingredients, categories and title
def including_and_excluding_ingredients_categories_and_title(includeIngredients:list, excludeIngredients:list, includeCategories:list, excludeCategories:list, page:int, title:str):
    """'includeIngredients': 'water, cinnamon',
  'excludeIngredients': 'beef, egg',"""
    import requests
    url = "https://api.foodoscope.com/recipe2-api/recipebyingredient/by-ingredients-categories-title"

    # Query parameters can also be passed as a dictionary to the params argument
    params = {
  'includeIngredients': includeIngredients,
  'excludeIngredients': excludeIngredients,
  'includeCategories': includeCategories,
  'excludeCategories': excludeCategories,
  'title': title,
  'page': page,
  'limit': 10
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
    }

    response = requests.get(
    url,
    params=params,
    headers=headers
    )

    return response.json()


#6 Recipe Instruction
def recipe_instruction(recipe_id: int):
  #this tool give the recipe instruction by taking input recipe id.
  import requests
  url = f"https://api.foodoscope.com/recipe2-api/instructions/{recipe_id}"

  headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
  }

  response = requests.get(
    url,
    headers=headers
  )

  return response.json()



#7 Ingredints information
def ingrendints(Recipe_id: int):
  import requests
  #this tool give the list of ingrendints that is use in dishes by taking input recipe id.
  url = f"https://api.foodoscope.com/recipe2-api/search-recipe/{Recipe_id}"

  headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
  }

  response = requests.get(
    url,
    headers=headers
  )
  x = response.json()
  ingredient_phrases = [item['ingredient_Phrase'] for item in x['ingredients']]
  return ingredient_phrases



#8 Recipe with title
def recipe_with_title(title:str):
    import requests
  #this tool give the recipe instruction by taking the input of recipe name(title).
    url = "https://api.foodoscope.com/recipe2-api/recipe-bytitle/recipeByTitle"

    # Query parameters can also be passed as a dictionary to the params argument
    params = {
  'title': title
}

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
}

    response = requests.get(
    url,
    params=params,
    headers=headers
)

    return response.json()



def file_maker(file_name: str, context: str):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    import os

    # 🔥 Ensure .pdf extension automatically
    if not file_name.lower().endswith(".pdf"):
        file_name = file_name + ".pdf"

    # 🔥 Optional: save inside a fixed folder
    save_dir = "generated_files"
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    text = c.beginText(50, height - 50)
    text.setFont("Helvetica", 11)

    # 🔥 Line-by-line writing
    for line in context.split("\n"):
        text.textLine(line)

        # Page overflow handling
        if text.getY() < 50:
            c.drawText(text)
            c.showPage()
            text = c.beginText(50, height - 50)
            text.setFont("Helvetica", 11)

    c.drawText(text)
    c.save()
    print(f"{file_name} saved successfully")
    return f"{file_name} saved successfully"




def meal_plane(calories_per_day:int,days:int):
  import requests
  url = "https://api.foodoscope.com/recipe2-api/mealplan/meal-plan"

  payload = {
    "calories_per_day": calories_per_day,
    "days": days
}

  headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ"
}

  response = requests.post(
    url,
    json=payload,
    headers=headers
)
  return response.json()