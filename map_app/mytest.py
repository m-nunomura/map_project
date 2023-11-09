import urllib
import requests

address = "富山城"

makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
s_quote = urllib.parse.quote(address)
response = response = requests.get(makeUrl + s_quote)
coordinated = response.json()[0]["geometry"]["coordinates"]
print(coordinated)