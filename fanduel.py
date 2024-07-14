import requests
import config
import standardizations
from collections import defaultdict

def get_fanduel_game_ids(sport):
    url = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId={sport}&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"
    response = requests.get(url, headers=config.fanduel_headers)
    data = response.json()
    game_IDs = []
    for event in data['attachments']['events'].values():
        eventID = event['eventId']
        game = event['name']
        if "@" in game: #only real matches have @, other events don't.
            game_IDs.append(eventID)
    return game_IDs

def get_fanduel_player_props(sport, game_id, player_props_dict):
    for stat_type in config.fanduel_player_prop_types[sport]:
        url = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId={game_id}&tab={stat_type}&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true"
        response = requests.get(url, headers=config.fanduel_headers)
        data = response.json()
        try: #this will throw an error for live games or other types that we don't want
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
                                        "line": line,
                                        "over": over,
                                        "under": under
                                    }
                player_props_dict[player_name][stat] = player_prop_item
            except:
                continue
    return player_props_dict

def main():
    fanduel_player_props_dict = defaultdict(dict)
    wnba_games = get_fanduel_game_ids('wnba')
    for game in wnba_games:
        fanduel_player_props_dict = get_fanduel_player_props('wnba', game, fanduel_player_props_dict)
    mlb_games = get_fanduel_game_ids('mlb')
    for game in mlb_games:
        fanduel_player_props_dict = get_fanduel_player_props('mlb', game, fanduel_player_props_dict)
    [print(noob) for noob in fanduel_player_props_dict.items()]
main()

# [print(noob) for noob in fanduel_player_props.items()]
