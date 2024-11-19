from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
import json
import pickle
import os


def get_dynamic_content(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        return driver.page_source
    finally:
        driver.quit()


def extract_recipe_details(url):
    html = get_dynamic_content(url)
    soup = BeautifulSoup(html, 'html.parser')

    recipe_details = {"title": "Recipe", "servings": "", "ingredients": []}

    # Try JSON-LD structured data
    json_ld = soup.find('script', type='application/ld+json')
    if json_ld:
        try:
            data = json.loads(json_ld.string)
            if isinstance(data, list): 
                for item in data:
                    if item.get('@type') == 'Recipe':
                        recipe_details.update({
                            "title": item.get("name", "Recipe"),
                            "servings": extract_servings_from_text(item.get("recipeYield", "")),
                            "ingredients": item.get("recipeIngredient", []),
                        })
                        return recipe_details
            elif data.get('@type') == 'Recipe':
                recipe_details.update({
                    "title": data.get("name", "Recipe"),
                    "servings": extract_servings_from_text(data.get("recipeYield", "")),
                    "ingredients": data.get("recipeIngredient", []),
                })
                return recipe_details
        except json.JSONDecodeError:
            pass

    # Fallback to HTML parsing
    recipe_details["title"] = fallback_extract_title(soup) or recipe_details["title"]
    recipe_details["servings"] = fallback_extract_servings(soup) or recipe_details["servings"]
    recipe_details["ingredients"] = fallback_html_ingredient_extraction(soup)

    return recipe_details


def fallback_extract_title(soup):
    title = soup.find("h1") or soup.find("title")
    return title.get_text(strip=True) if title else None


def fallback_extract_servings(soup):
    keywords = ["serves", "yield", "makes"]
    tags = soup.find_all(["div", "span", "p"])
    for tag in tags:
        text = tag.get_text(strip=True).lower()
        if any(keyword in text for keyword in keywords):
            match = re.search(r'\d+', text)
            if match:
                return int(match.group())
    return None


def extract_servings_from_text(text):
    match = re.search(r'\d+', str(text))
    return int(match.group()) if match else None


def fallback_html_ingredient_extraction(soup):
    #Specific classes for ingredients
    ingredients = []
    ingredients_section = soup.find_all('li', class_='wprm-recipe-ingredient')
    if ingredients_section:
        for item in ingredients_section:
            amount = item.find('span', class_='wprm-recipe-ingredient-amount')
            unit = item.find('span', class_='wprm-recipe-ingredient-unit')
            name = item.find('span', class_='wprm-recipe-ingredient-name')
            notes = item.find('span', class_='wprm-recipe-ingredient-notes')

            ingredient = ' '.join(filter(None, [
                amount.get_text(strip=True) if amount else '',
                unit.get_text(strip=True) if unit else '',
                name.get_text(strip=True) if name else '',
                f"({notes.get_text(strip=True)})" if notes else ''
            ]))
            if ingredient:
                ingredients.append(ingredient)
        return ingredients

    #General "Ingredients" section
    heading = soup.find(lambda tag: tag.name in ["h2", "h3", "h4"] and "Ingredients" in tag.text)
    if heading:
        for sibling in heading.find_next_siblings():
            if sibling.name and sibling.name.startswith("h"):
                break
            if sibling.name in ["ul", "ol"]:
                ingredients.extend(item.get_text(strip=True) for item in sibling.find_all("li"))
    return ingredients

def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    creds = None

    # Load credentials from file
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Refresh or request new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('tasks', 'v1', credentials=creds)


def sync_to_google_tasks(service, recipe_details):
    # Create a task list with the recipe title and servings
    task_list_title = f"{recipe_details['title']} ({recipe_details['servings']})"
    task_lists = service.tasklists().list().execute()

    task_list = next((tl for tl in task_lists.get('items', []) if tl['title'] == task_list_title), None)
    if not task_list:
        task_list = service.tasklists().insert(body={'title': task_list_title}).execute()

    # Add each ingredient as a task
    for ingredient in recipe_details['ingredients']:
        service.tasks().insert(tasklist=task_list['id'], body={'title': ingredient}).execute()


if __name__ == '__main__':
    url = input("Enter the recipe URL: ")
    recipe_details = extract_recipe_details(url)

    if recipe_details["ingredients"]:
        print(f"Recipe Title: {recipe_details['title']}")
        print(f"Servings: {recipe_details['servings']}")
        print("Ingredients:")
        for i, ingredient in enumerate(recipe_details["ingredients"], 1):
            print(f"{i}. {ingredient}")

        # Authenticate and sync to Google Tasks
        service = authenticate()
        sync_to_google_tasks(service, recipe_details)
        print("Ingredients have been synced to Google Tasks!")
    else:
        print("Could not extract recipe details. Please check the URL.")