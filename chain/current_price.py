import requests
import json

response = requests.get("https://api.coinbase.com/v2/prices/spot?currency=USD")
print(json.dumps(json.loads(response.text), indent=1))