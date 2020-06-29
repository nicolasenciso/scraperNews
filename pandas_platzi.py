import pandas as pd
import csv
from urllib.parse import urlparse

el_universal = pd.read_csv('eluniversal_2020_06_03_articles.csv')


el_universal['newspaper_uid'] = 'eluniversal'

el_universal['host'] = el_universal['url'].apply(lambda url: urlparse(url).netloc)


test = el_universal['host'].value_counts()
print(el_universal)
print(test)