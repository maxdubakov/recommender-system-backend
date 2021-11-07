import time

import numpy as np
import torch

from config import Config


def get_hit_ratio(ratings, test_ratings, model, all_beer_ids):
    if Config.verbose:
        print('Preparing test data...')
    test_user_item_set = set(zip(test_ratings['user_id'], test_ratings['beer_id']))

    # Dict of all items that are interacted with by each user
    user_interacted_items = ratings.groupby('user_id')['beer_id'].apply(list).to_dict()

    if Config.verbose:
        print('Done.')
        print(f'Calculating The Hit Ratio @{Config.hit_ratio}...')
    hits = []
    start_time = round(time.time() * 1000)
    for (u, i) in test_user_item_set:
        interacted_items = user_interacted_items[u]
        not_interacted_items = set(all_beer_ids) - set(interacted_items)
        selected_not_interacted = list(np.random.choice(list(not_interacted_items), 99))
        test_items = selected_not_interacted + [i]

        predicted_labels = np.squeeze(model(torch.tensor([u] * 100),
                                            torch.tensor(test_items)).detach().numpy())

        top_n_items = [test_items[i] for i in np.argsort(predicted_labels)[::-1][0:Config.hit_ratio].tolist()]

        if i in top_n_items:
            hits.append(1)
        else:
            hits.append(0)
    required_time = round(time.time() * 1000) - start_time
    if Config.verbose:
        print(f'Required Time: {required_time} (ms)')
        print('Done.')

    hit_ratio = round(np.average(hits), 2)
    print(f'The Hit Ratio @{Config.hit_ratio} is {hit_ratio}')
    return hit_ratio


def predict(model, all_beer_ids, user_id, n):
    preds = np.squeeze(model(torch.tensor([user_id] * len(all_beer_ids)),
                             torch.tensor(all_beer_ids)).detach().numpy())
    top_n_items = [all_beer_ids[i] for i in np.argsort(preds)[::-1][0:n].tolist()]
    return top_n_items
