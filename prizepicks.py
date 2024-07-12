import requests
from collections import defaultdict
from config import prizepicks_mlb_url, prizepicks_wnba_url, prizepicks_headers

def get_prizepicks_player_props(url, headers, player_props_dict):
    """
    Fetches Prizepicks player props from the given URL and populates the player props dictionary 
    Format of output: Each player has a dictionary of their props {player: {stat type: line}}
    """
    response = requests.get(url, headers=headers)
    data = response.json()
    players_info = {} 
    for player in data['included']:
        """
        Map each player ID to the json data associated (player name, team, id, etc).
        The primary function is allowing us to later access player name by their 
        player ID, since the prop info contains only the ID and not the name.
        """
        players_info[player['id']] = player['attributes']
    prop_data = [] #list of each prop with below information 
    for prop in data['data']:
        """
        Put all props into prop_data list (list of dicts). 
        Keep only standard bets (no demons/goblins, no promos). 
        """
        if prop['attributes']['odds_type'] != "standard": 
            continue
        player_id = prop['relationships']['new_player']['data']['id']
        promo = prop['attributes']['is_promo']
        line = prop['attributes']['line_score']
        stat_type = prop['attributes']['stat_type']
        prop_data.append({'player_id': player_id, 'promo': promo, 'line': line, 'stat_type': stat_type})
    for prop in prop_data: #### I CAN PROBABLY COMBINE THIS WITH ABOVE THE LIST IS NOT NECESSARY....
        if prop['promo']: #do nothing for now but maybe later handle some other way
            continue
        player_name = players_info[prop['player_id']]['display_name']
        line = prop['line']
        stat = prop['stat_type']
        if "Combo" in stat: #ensure only looking at single player bets
            continue
        player_props_dict[player_name][stat] = line 

def main():
    prizepicks_player_props_dict = defaultdict(dict) #map player name to dict of their bets 
    try:
        get_prizepicks_player_props(prizepicks_mlb_url, prizepicks_headers, prizepicks_player_props_dict)
    except Exception as e: #likely no live games?
        print(f"Error accessing MLB: {e}")
    try:
        get_prizepicks_player_props(prizepicks_wnba_url, prizepicks_headers, prizepicks_player_props_dict)
    except Exception as e: #likely no live games?
        print(f"Error accessing WNBA: {e}")
    if prizepicks_player_props_dict == defaultdict(dict): 
        return None 
    else: 
        return prizepicks_player_props_dict
    
if __name__ == "__main__":
    prizepick_props = main()
    if prizepick_props:
        print(f"Prizepicks props")
        print('-' * 50)
        [print(prop) for prop in prizepick_props.items()]
    else:
        print("Unable to access props")

    





