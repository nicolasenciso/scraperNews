import argparse
import logging
import hashlib
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__)


def main(filename):
    logger.info('starting cleaning process')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)

    return df


def _extract_host(df):
    logger.info('extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df

def _remove_new_lines_from_body(df):
    logger.info('remove new lines from body')

    stripped_body =  (df
                        .apply(lambda row: row['body'], axis=1)
                        .apply(lambda body: list(body))
                        .apply(lambda letters: list(map(lambda letter: letter.replace('\n',''),letters)))
                        .apply(lambda letters: list(map(lambda letter: letter.replace('\r',''), letters)))
                        .apply(lambda letters: ''.join(letters))
                     )

    df['body'] = stripped_body

    return df


def _generate_uids_for_rows(df):
    logger.info('generating uids for each row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
           )

    df['uids'] = uids

    return df.set_index('uids')


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename)

def _extract_newspaper_uid(filename):
    logger.info('extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]

    logger.info('newspaper uid detected {}'.format(newspaper_uid))
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('filling newspaper_uid columns with {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid

    return df


def _fill_missing_titles(df):
    logger.info('filling missing titles')
    missing_titles_mask = df['title'].isna()

    missing_titles = (df[missing_titles_mask]['url']
                    .str.extract(r'(?P<missing_titles>[^/]+)$')
                    .applymap(lambda title: title.split('-'))
                    .applymap(lambda title_word_list: ' '.join(title_word_list))
                    )

    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',help='The path to the dirty data', type=str)

    args = parser.parse_args()
    df = main(args.filename)
    print(df)