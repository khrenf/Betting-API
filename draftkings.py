import requests
from collections import defaultdict

headers = {
    "Origin": "https://sportsbook.draftkings.com",
    "Priority": "u=1, i",
    "Referer": "https://sportsbook.draftkings.com/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
}
# url = 'https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/84240?format=json'


# response = requests.get(url, headers=headers)
# data = response.json()
# game_IDs = []
# next_not_started_game_date = None
# for event in data['eventGroup']['events']:
#     start_date = event['startDate'][:10] #get in format 2024-07-13
#     #if needed process based on date here 
#     if event['eventStatus']['state'] == "STARTED":
#         continue
#     game_IDs.append(event['eventId'])


# draftkings_player_props = defaultdict(dict)
# url = 'https://sportsbook-ca-on.draftkings.com/api/team/markets/dkusil/v3/event/'
# for game_ID in game_IDs:
#     game_url = url + game_ID + "?format=json"
#     response = requests.get(game_url, headers=headers)
#     data = response.json()
#     for category in data['eventCategories']:
#         if (category['name'] == "Batter Props") or (category['name'] == "Pitcher Props"):
#             for props_by_stat_type in category['componentizedOffers']:
#                 stat = props_by_stat_type['subcategoryName']
#                 #here we would check if the stat type is one we want but for now ignore
#                 for player_prop in props_by_stat_type['offers'][0]:
#                     try:
#                         player_name = player_prop['playerNameIdentifier']
#                         over = player_prop['outcomes'][0]['oddsAmerican']
#                         under = player_prop['outcomes'][1]['oddsAmerican']
#                         line = player_prop['outcomes'][1]['line']
#                         player_prop_item = {
#                             "line": line,
#                             "over": over,
#                             "under": under
#                         }
#                         draftkings_player_props[player_name][stat] = player_prop_item
#                         #this might handle it automatically since it won't do anything if empty
#                     except: #probably a combo bet or something where this playername field doesn't exist
#                         pass



wnba_url = 'https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/94682?format=json'
response = requests.get(wnba_url, headers=headers)
data = response.json()
wnba_game_IDs = []
next_not_started_game_date = None
for event in data['eventGroup']['events']:
    start_date = event['startDate'][:10] #get in format 2024-07-13
    #if needed process based on date here 
    if event['eventStatus']['state'] == "STARTED":
        continue
    wnba_game_IDs.append(event['eventId'])


draftkings_player_props = defaultdict(dict)
url = 'https://sportsbook-ca-on.draftkings.com/api/team/markets/dkusil/v3/event/'
for game_ID in wnba_game_IDs:
    game_url = url + game_ID + "?format=json"
    response = requests.get(game_url, headers=headers)
    data = response.json()
    for category in data['eventCategories']:
        for props_by_stat_type in category['componentizedOffers']:
            stat = props_by_stat_type['subcategoryName']
            #here we would check if the stat type is one we want but for now ignore
            for player_prop in props_by_stat_type['offers'][0]:
                try:
                    player_name = player_prop['playerNameIdentifier']
                    over = player_prop['outcomes'][0]['oddsAmerican']
                    under = player_prop['outcomes'][1]['oddsAmerican']
                    line = player_prop['outcomes'][1]['line']
                    player_prop_item = {
                        "line": line,
                        "over": over,
                        "under": under
                    }
                    draftkings_player_props[player_name][stat] = player_prop_item
                    #this might handle it automatically since it won't do anything if empty
                except: #probably a combo bet or something where this playername field doesn't exist
                    pass
[print(prop) for prop in draftkings_player_props.items()]
