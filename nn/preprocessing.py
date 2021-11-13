import pickle as pkl

import numpy as np
import pandas as pd

try:
    from config import Config
except ImportError:
    from .config import Config


def read():
    return pd.read_csv(Config.data_path, parse_dates=Config.date_cols)


def str_to_id(ratings: pd.DataFrame, col_name: str, new_col_name):
    unique_values = ratings[col_name].unique()
    name_to_int = dict(zip(ratings[col_name].unique(), range(len(unique_values))))

    pkl.dump(name_to_int, open('./models/review_profilename_to_user_id.pkl', 'wb+'), protocol=pkl.HIGHEST_PROTOCOL)

    ratings[new_col_name] = ratings[col_name].apply(lambda name: name_to_int[name])
    return ratings


def process():
    if Config.verbose:
        print(f'Loading the dataset {Config.dataset_name}...')
    ratings = read()
    if Config.verbose:
        print('Done.')

    if Config.verbose:
        print(f'Processing the dataset {Config.dataset_name}...')
    ratings.drop('brewery_id', axis=1, inplace=True)
    ratings.drop('brewery_name', axis=1, inplace=True)
    ratings.drop('review_overall', axis=1, inplace=True)
    ratings.drop('review_aroma', axis=1, inplace=True)
    ratings.drop('review_appearance', axis=1, inplace=True)
    ratings.drop('beer_style', axis=1, inplace=True)
    ratings.drop('review_palate', axis=1, inplace=True)
    ratings.drop('beer_name', axis=1, inplace=True)
    ratings.drop('beer_abv', axis=1, inplace=True)
    ratings = str_to_id(ratings, 'review_profilename', 'user_id')
    ratings.drop('review_profilename', axis=1, inplace=True)

    rand_user_ids = np.random.choice(ratings['user_id'].unique(),
                                     size=int(len(ratings['user_id'].unique()) * Config.part_of_dataset_used),
                                     replace=False)
    ratings = ratings.loc[ratings['user_id'].isin(rand_user_ids)]
    if Config.verbose:
        print('There are {} rows of data from {} users'.format(len(ratings), len(rand_user_ids)))

    ratings[Config.rank_latest] = ratings \
        .groupby(['user_id'])['review_time'] \
        .rank(method='first', ascending=False)

    ratings.rename(columns={'beer_beerid': 'beer_id', 'review_taste': 'rating'}, inplace=True)
    if Config.verbose:
        print('Done.')
    return ratings


def train_test_split(ratings):
    if Config.verbose:
        print(f'Splitting the dataset {Config.dataset_name}...')
    train_ratings = ratings[ratings[Config.rank_latest] != 1]
    test_ratings = ratings[ratings[Config.rank_latest] == 1]

    train_ratings = train_ratings[['user_id', 'beer_id', 'rating']]
    test_ratings = test_ratings[['user_id', 'beer_id', 'rating']]
    train_ratings.loc[:, 'rating'] = 1
    if Config.verbose:
        print('Done.')
    return train_ratings, test_ratings


def eliminate_duplicated_ids(data: pd.DataFrame):

    beer_name_id: pd.DataFrame = data[['beer_beerid', 'beer_name']].drop_duplicates()
    print(f'Before: {len(beer_name_id)}')
    repeated_ids = beer_name_id.groupby('beer_name').count().sort_values('beer_beerid', ascending=False)
    repeated_ids = list(repeated_ids[repeated_ids['beer_beerid'] > 1]['beer_beerid'].to_dict().keys())
    unique_name_to_id = dict()
    for row in beer_name_id.iterrows():
        beer_name = row[1]['beer_name']
        beer_id = row[1]['beer_beerid']
        if beer_name not in unique_name_to_id.keys() and beer_name in repeated_ids:
            unique_name_to_id[beer_name] = beer_id

    for _name, _id in unique_name_to_id.items():
        data['beer_beerid'][data['beer_name'] == _name] = _id

    print(f"After: {len(data[['beer_beerid', 'beer_name']].drop_duplicates())}")
    data.to_csv('./data/beer_new_reviews.csv')


if __name__ == '__main__':
    eliminate_duplicated_ids(read())
