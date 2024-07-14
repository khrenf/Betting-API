import requests
import config
from collections import defaultdict

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://www.pinnacle.com/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "X-Api-Key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
    "X-Device-Uuid": "203b12d5-95d2a746-d9f249b8-3a73e1d3"
}
url = "https://guest.api.arcadia.pinnacle.com/0.1/leagues/246/matchups?brandId=0"
response = requests.get(url, headers=headers)
data = response.json()
print(data)