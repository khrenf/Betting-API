import requests
from collections import defaultdict

game_url = 'https://sportsbook-nash.draftkings.com/api/sportscontent/views/dkusil//v1/sports/7/live' #7 = baseball

response = requests.get(game_url)
data = response.json()
"""
Iterate through the first featured subcategory (0) which has all games and add the eventId of each
game to a list. This will allow us to generate the url for API calls to props in each game
"""
games = []
[games.append(game['eventId']) for game in data['featuredDisplayGroup']['featuredSubcategories'][0]['events']]
print(games)

for game in games:
    url = 'https://sportsbook-ca-on.draftkings.com/api/team/markets/dkusil/v3/event/30787502?format=json'
    #something like this but with the game id in that number spot