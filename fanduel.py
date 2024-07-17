import requests
import resources.config as config
import resources.standardizations as standardizations
from collections import defaultdict

def get_fanduel_game_ids(sport):
    """
    Returns list of game IDs. Fetches from JSON containing available event information for a given sport.
    Filters out most non-game events.
    """
    url = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId={sport}&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"
    response = requests.get(url, headers=config.fanduel_headers)
    data = response.json()
    game_IDs = []
    for event in data['attachments']['events'].values():
        try: #handle unknown event type throwing error, with different output format
            eventID = event['eventId']
            game = event['name']
            if "@" in game: #only real matches have @, other events don't.
                game_IDs.append(eventID)
        except:
            continue
    return game_IDs

def get_fanduel_player_props(sport, game_id, player_props_dict):
    """
    Returns updated player prop dict containing players mapped to dictionaries of their bets and lines.
    Accepts a list of game IDs and what sport they correspond to. Modifies and standardizes format of 
    player names, stat types, etc. Handles errors related to started games, special events, missing bet
    information on page (like if a starting pitcher isn't declared yet..)
    """
    for stat_type in config.fanduel_player_prop_types[sport]:
        url = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId={game_id}&tab={stat_type}&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true"
        response = requests.get(url, headers=config.fanduel_headers)
        try: #this will throw an error for live games or other types that we don't want
            data = response.json()
            data['attachments']['markets']
        except:
            print(game_id)
            continue
        for market_id in data['attachments']['markets']:
            """ 
            try-catch will handle a variety of errors: live-game, non-standard game, 
            stat type we don't care about, etc
            """
            try: 
                market = (data['attachments']['markets'][market_id])
                stat = market['marketName']
                if "-" not in stat: #individual player props will have - in stat name
                    if "Outs Recorded" in stat:
                        stat = "Outs Recorded"
                    else:
                        continue
                #stat will be in format Kelsey Plum - Pts + Ast - we want the second 'half'
                stat = market['marketName'].split(' - ')[-1]
                stat = standardizations.fanduel_standardized_props[stat]
                #runnername format: Kelsey Plum Over - remove "over" to handle case of 3 word name
                player_name = ' '.join(market['runners'][0]['runnerName'].split()[:-1]) 
                line = market['runners'][0]['handicap']
                over = market['runners'][0]['winRunnerOdds']['americanDisplayOdds']['americanOdds']
                under = market['runners'][1]['winRunnerOdds']['americanDisplayOdds']['americanOdds']
                over = "+" + str(over) if over > 0 else str(over)
                under = "+" + str(under) if under > 0 else str(under)
                player_prop_item = {
                                        "line": float(line),
                                        "over": over,
                                        "under": under
                                    }
                player_props_dict[player_name][stat] = player_prop_item
            except: #just continue, most errors caused by unwanted market type (1st inning outs etc)
                continue
    return player_props_dict

def main():
    """
    Returns player prop dictionary. Fetches game IDs for each sport, 
    for each game gets props and adds to dict.
    """
    fanduel_player_props_dict = defaultdict(dict)
    wnba_games = get_fanduel_game_ids('wnba')
    for game in wnba_games:
        fanduel_player_props_dict = get_fanduel_player_props('wnba', game, fanduel_player_props_dict)
    mlb_games = get_fanduel_game_ids('mlb')
    for game in mlb_games:
        fanduel_player_props_dict = get_fanduel_player_props('mlb', game, fanduel_player_props_dict)
    if fanduel_player_props_dict == defaultdict(dict):
        return None
    return fanduel_player_props_dict

if __name__ == "__main__":
    fanduel_props = main()
    if fanduel_props:
        [print(prop) for prop in fanduel_props.items()]
