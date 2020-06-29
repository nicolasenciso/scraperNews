import pandas as pd
import csv
from urllib.parse import urlparse

el_universal = pd.read_csv('eluniversal_2020_06_03_articles.csv')


el_universal['newspaper_uid'] = 'eluniversal'

el_universal['host'] = el_universal['url'].apply(lambda url: urlparse(url).netloc)


test = el_universal['host'].value_counts()
print(el_universal)
print(test)


missing_titles_mask = el_universal['title'].isna()

missing_titles = (el_universal[missing_titles_mask]['url']
    .str.extract(r'(?P<missing_titles>[^/]+)$')
    .applymap(lambda title: title.split('-'))
    .applymap(lambda title_word_list: ' '.join(title_word_list))
    )

print(missing_titles)