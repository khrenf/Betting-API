import requests
from collections import defaultdict
from config import underdog_url
from standardizations import underdog_standardized_props

def get_underdog_player_props(url, player_props_dict):
    """
    Fetches Underdog Fantasy player props from the given URL and populates the player props dictionary 
    Format of output: Each player has a dictionary of their props {player: {stat type: line}}
    """
    response = requests.get(url)
    data = response.json()
    active_players = set() 
    for player in data['players']: 
        """
        Since the prop data has no info about the sport, we populate a set with players who have
        active props in sports we are interested in.
        """
        if player['sport_id'] == 'MLB' or (player['sport_id'] == 'WNBA'):
            player_name = player['first_name'] + " " + player['last_name']
            active_players.add(player_name)
    for prop in data['over_under_lines']:
        """
        Now go through each prop available on Underdog and check if the player is in our players set and if
        the multiplier is 1.0 since we only want standard payout bets. Then we extract name + relevant 
        info and add to the player props dictionary.
        """
        payout_multiplier = prop['options'][0]['payout_multiplier']
        if payout_multiplier != "1.0":
            continue 
        line = prop['stat_value']
        prop_info = prop['over_under']['title'].split()
        prop_info = prop_info[:-1] #remove o/u which is the last element
        player_name = prop_info[0] + " " + prop_info[1]
        if (player_name not in active_players):
            continue
        try_stat, stat = ' '.join(prop_info[2:]), None
        if try_stat in underdog_standardized_props: #handle case of name being more than 2 words, skip these for now
            stat = underdog_standardized_props[try_stat]
        else:
            continue
        player_props_dict[player_name][stat] = line
    return player_props_dict
        
def main():
    """
    Create and populate the underdog props dictionary. Exceptions likely indicate no bets available for any 
    sports we are interested in, so return None in that case.
    """
    underdog_player_props = defaultdict(dict)
    try:
        get_underdog_player_props(underdog_url, underdog_player_props)
    except Exception as e: 
        print(f"Error accessing props: {e}")
    if underdog_player_props == defaultdict(dict): 
        return None 
    else: 
        return underdog_player_props

if __name__ == "__main__":
    underdog_props = main()
    if underdog_props:
        print(f"Underdog props")
        print("-" * 50)
        [print(prop) for prop in underdog_props.items()]
    else:
        print("Unable to access props")

