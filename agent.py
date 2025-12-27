import tool
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

def agent(prompt, user_query, user_email=None):
    # 1. Break Circular Import: Import mail ONLY when needed
    from test import mail 
    
    # Standard tool setup
    protein = tool.protein
    Energy = tool.Energy
    Carbs = tool.Carbs
    diet_by_region = tool.diet_by_region
    recipe_instruction = tool.recipe_instruction
    ingrendints = tool.ingrendints
    recipe_with_title = tool.recipe_with_title
    file_maker = tool.file_maker
    meal_plane = tool.meal_plane

    load_dotenv()
    api_key = os.getenv("API_KEY")

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        tools=[protein, recipe_instruction, Energy, Carbs, diet_by_region, 
               ingrendints, recipe_with_title, file_maker, meal_plane])

    combined_user_content = f"user query-- {user_query}"

    contents_for_generation = [
        types.Content(role="model", parts=[types.Part(text=prompt)]),
        types.Content(role="user", parts=[types.Part(text=combined_user_content)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents_for_generation,
        config=config,
    )

    try:
        final_text = response.text
        
        # 2. AUTOMATIC MAIL TRIGGER
        # If the app provided an email, send the result automatically
        if user_email and final_text:
            mail(final_text, user_email)
            print(f"Agent: Successfully mailed result to {user_email}")
            
        return final_text
    except Exception as e:
        return f"model response error {e}"