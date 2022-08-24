import requests
import json
from pprint import pprint
import configparser

config = configparser.ConfigParser()
config.read('.env')
api_key = config['api']['NOTION_KEY']
database_id = config['api']['NOTION_DATABASE_ID']

def print_json(json_str: str):
    """
    Takes json and returns it as a nice, indented string

    Args:
        str: raw inputted json string
    """
    obj = json.loads(json_str)
    print(json.dumps(obj, indent=4))


def retrieve_database() -> str:
    url = "https://api.notion.com/v1/databases/" + database_id + "/query"

    payload = {"page_size": 100}
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, json=payload, headers=headers).text
    return response


def process_database(response: str):
    """
    Extracts useful information out of Notion API response

    Args:
        response (str): JSON text response from database GET request, usually from retreive_database()

    Returns:
        (pages, columns) pair where each is a list of id's
    """
    columns = {}
    pages = []
    json_obj = json.loads(response)

    for row in json_obj["results"]:
        pages.append(row["id"])
    
    for col in json_obj["results"][0]["properties"]:
        columns[col] = row["properties"][col]["id"]

    return (pages, columns)


def retrieve_value(page_id: str, property_id: str) -> str:
    """
    Given id's for row/column, returns the value at that location

    Args:
        page_id (str): id for the row/gym entry
        property_id (str): id for the column/gym activity

    Returns:
        str: notion api response for value at given location
    """
    url: str = "https://api.notion.com/v1/pages/" + page_id + "/properties/" + property_id

    headers: str = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": "Bearer " + api_key
    }

    response: str = requests.get(url, headers=headers).text

    return response

