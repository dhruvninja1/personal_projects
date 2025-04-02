import requests
from bs4 import BeautifulSoup
url = "https://weather.com/"

response = requests.get(url)


if response.status_code == 200:
    html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")




things = soup.find("div", class_="CurrentConditions--tempValue--zUBSz")
print(things.text)