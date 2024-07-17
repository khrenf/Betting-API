import requests
from collections import defaultdict
import resources.config as config

def get_prizepicks_player_props(player_props_dict):
    """
    Fetches Prizepicks player props from the given URL and populates the player props dictionary 
    Format of output: Each player has a dictionary of their props {player: {stat type: line}}
    """
    for sport_ID in config.prizepicks_sport_IDs:
        url = f"https://api.prizepicks.com/projections?league_id={sport_ID}&per_page=250&single_stat=true"
        response = requests.get(url, headers=config.prizepicks_headers)
        try:
            data = response.json()
            if not data.get('data'): #sometimes returns data if no sport is open, so check here 
                # print(f"No data available for sport ID: {sport_ID}")
                continue
        except: #sport has no props available
            continue
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
            player_props_dict[player_name][stat] = float(line)

def main():
    """
    Returns player props dictionary, filled by function which will look for available bets 
    in any specified league from config file. 
    """
    prizepicks_player_props_dict = defaultdict(dict) #map player name to dict of their bets 
    get_prizepicks_player_props(prizepicks_player_props_dict)
    if prizepicks_player_props_dict == defaultdict(dict):
        return None
    return prizepicks_player_props_dict
main()
    
if __name__ == "__main__":
    prizepick_props = main()
    if prizepick_props:
        print(f"Prizepicks props")
        print('-' * 50)
        [print(prop) for prop in prizepick_props.items()]
    else:
        print("Unable to access props")

    





