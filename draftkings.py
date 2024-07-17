import requests
from collections import defaultdict
import resources.standardizations as standardizations
import resources.config as config
from typing import List

def get_draftkings_game_IDs(sport_IDs: List[str]):
    """
    Iterate through each sport ID code to extract data about each upcoming event, ignore live games.
    Return a list of each upcoming game's ID, which is needed to build API requests for each game.
    """
    game_IDs = []
    for sport_ID in sport_IDs:
        try:
            url = f"https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/{sport_ID}?format=json"
            response = requests.get(url, headers=config.draftkings_headers)
            data = response.json()
            for event in data['eventGroup']['events']:
                start_date = event['startDate'][:10] #get in format 2024-07-13
                #if needed process based on date here 
                if event['eventStatus']['state'] == "STARTED":
                    continue
                game_IDs.append(event['eventId'])
        except: 
            continue
    return game_IDs
    
def get_draftkings_player_props(game_IDs: List[str]):
    """
    Iterate through each upcoming game. Within a game, iterate through props available for each type
    of stat we're interested in (ones offered on other platforms like PrizePicks). Handle initial 
    request errors in case the game isn't available yet, and handle errors when trying to access player 
    name - if there is an error accessing player name it means it's a combo or type of bet we don't care
    about. Extract O/U, stat type, and line for each prop, add that as a dictionary to our larger prop 
    dictioanry and return that.
    """
    player_props_dict = defaultdict(dict)
    for game_ID in game_IDs:
        game_url = f"https://sportsbook-ca-on.draftkings.com/api/team/markets/dkusil/v3/event/{game_ID}?format=json"
        response = requests.get(game_url, headers=config.draftkings_headers)
        try:
            data = response.json()
        except:
            continue
        for category in data['eventCategories']:
            for props_by_stat_type in category['componentizedOffers']:
                stat = props_by_stat_type['subcategoryName']
                if stat not in standardizations.draftkings_standardized_props:
                    continue
                stat = standardizations.draftkings_standardized_props[stat]
                for player_prop in props_by_stat_type['offers'][0]:
                    try:
                        player_name = player_prop['playerNameIdentifier']
                        over = player_prop['outcomes'][0]['oddsAmerican']
                        under = player_prop['outcomes'][1]['oddsAmerican']
                        line = player_prop['outcomes'][1]['line']
                        player_prop_item = {
                            "line": float(line),
                            "over": over,
                            "under": under
                        }
                        player_props_dict[player_name][stat] = player_prop_item
                        #this might handle it automatically since it won't do anything if empty
                    except: #probably a combo bet or something where this playername field doesn't exist
                        pass
    return player_props_dict

def main():
    """
    Fetch all upcoming games IDs --> build player props dictionary from props in each game
    """
    all_game_IDs = get_draftkings_game_IDs(config.draftkings_sport_IDs)
    draftkings_props = get_draftkings_player_props(all_game_IDs)
    if draftkings_props == defaultdict(dict):
        return None
    return draftkings_props

if __name__ == "__main__":
    draftkings_props = main()
    if draftkings_props:
        [print(prop) for prop in draftkings_props.items()]
