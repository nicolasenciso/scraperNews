import requests
import bs4

response = requests.get('http://eltiempo.com')

soup = bs4.BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))