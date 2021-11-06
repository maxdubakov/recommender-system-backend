from preprocessing import train_test_split, process as process_data
from train import train
from test import get_hit_ratio

from beer.models import Beer


def main():
    beer = Beer(name='New beer')
    # beer.save()
    # ratings = process_data()
    # train_ratings, test_ratings = train_test_split(ratings)
    #
    # num_users = ratings['user_id'].max()+1
    # num_items = ratings['beer_id'].max()+1
    # all_beer_ids = ratings['beer_id'].unique()
    #
    # model = train(num_users, num_items, train_ratings, all_beer_ids)
    # hit_ratio = get_hit_ratio(ratings, test_ratings, model, all_beer_ids)
    # return hit_ratio


if __name__ == '__main__':
    main()
