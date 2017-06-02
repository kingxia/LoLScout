# query.py
# Make queries and handle errors to Riot API

import json
import time
import urllib
from query_exceptions import *

def query_riot_api(query):
    """Returns JSON from querying Riot API.

    Throws API errors with well-formatted JSON."""
    web_data = urllib.urlopen(query)
    raw_data = [line.strip() for line in web_data.readlines()]
    try:
        json_data = json.loads(raw_data[0])
    except ValueError:
        raise_exception(404)

    if 'status' in json_data.keys():
        if 'status_code' not in json_data['status'].keys():
            raise Exception("Poorly formatted data returned on query: " + str(query))
        else:
            raise_exception(json_data['status']['status_code'])

    return json_data

def query_with_retries(query, retries=3):
    """Query Riot API and retry on error 429.

    After [[retries]] attempts, returns an empty map."""
    response = {}
    for i in range(retries):
        try:
            response = query_riot_api(query)
            break
        except q429Exception:
            print "\tRate limit exceeded, waiting 10 seconds..."
            time.sleep(10)
    return response

def response_has_key(response, key):
    """Returns the value

summoner_name_query = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s?api_key=%s"
def get_summoner_id(summoner_name, api_key):
    """Returns the ID associated with the summoner name provided.

    Throws 400, 401, 404, 429, 501, 503, and generic exceptions."""

    query_name = summoner_name.replace(" ", "%20").lower()
    response_name = summoner_name.replace(" ", "").lower()
    query = summoner_name_query % (query_name, api_key)
    summoner_id = query_with_retries(query)
    
    if "id" not in summoner_id.keys():
        raise Exception("Incorrect data returned.\nQuery:\n%s\nResponse:\n%s" % (query, summoner_id))

    return summoner_id["id"]

# Distinct from summoner account id query
summoner_id_query = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/%s?api_key=%s"
def get_summoner_names(summoner_ids, api_key):
    """Returns the name associated with the provided ID.

    Throws 400, 401, 404, 429, 501, 503, and generic exceptions."""

    names = []
    if len(summoner_ids) == 0:
        return names

    for summoner_id in summoner_ids:
        query = summoner_id_query % (summoner_id, api_key)
        summoner_name = query_with_retries(query)
        if "name" not in summoner_name.keys():
            raise Exception("In
        names.append(summoner_name["name"].title())
    return names