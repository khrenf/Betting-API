prizepicks_sport_IDs = ['2', '3', '5'] # 2=MLB, 3=WNBA, 5=TENNIS
prizepicks_headers = {
    "Connection": "keep-alive",
    "Accept": "application/json; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Access-Control-Allow-Credentials": "true",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "Sec-Fetch-User",
    "Referer": "https://app.prizepicks.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}
underdog_url = 'https://api.underdogfantasy.com/beta/v5/over_under_lines'
underdog_sport_IDs = ['MLB', 'WNBA', 'TENNIS']
draftkings_headers = {
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
draftkings_sport_IDs = ['84240', '94682'] #84240 = MLB, 94682 = WNBA
fanduel_headers = {
        "Accept": "application/json",
        "Referer": "https://sportsbook.fanduel.com/",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
fanduel_player_prop_types = {
    'wnba': ['player-points', 'player-rebounds', 'player-assists', 'player-threes', 'player-combos'],
    'mlb': ['pitcher-props']
    }
pinnacle_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://www.pinnacle.com/",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}