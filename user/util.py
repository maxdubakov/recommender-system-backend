import os
import pickle as pkl
from datetime import datetime

import torch
import pytz

from beer.models import Beer
from user.models import User
from nn.NCF import NCF
from nn.config import Config


def format_results(results_with_beer_ids):
    results_with_beers = []
    for beer_id, rating in results_with_beer_ids:
        beer = Beer.objects.get(id=beer_id)
        categories = beer.category_set.all()
        if len(categories) > 0:
            category = categories[0].name
        else:
            category = 'Uncategorized'  # Should never happen

        results_with_beers.append(
            {
                'beer_id': beer.id,
                'beer_name': beer.name,
                'category': category,
                'rating': rating
            })
    return results_with_beers


def users():
    return len(User.objects.all())


def beers():
    return len(Beer.objects.all())


def all_beer_ids():
    return pkl.load(open('./nn/models/all_beer_ids.pkl', 'rb'))


def load_model():
    try:
        model = NCF(Config.DEFAULT_NUM_USERS, Config.DEFAULT_NUM_ITEMS, [], all_beer_ids())
        model.load_state_dict(torch.load(Config.load_path))
        model.eval()
        return model
    except Exception as e:
        print(str(e))
        return None


def load_last_time_trained():
    return pkl.load(open('./nn/data/last_time_trained.pkl', 'rb'))


def save_last_time_trained(_datetime):
    pkl.dump(_datetime,
             open('./nn/data/last_time_trained.pkl', 'wb+'),
             protocol=pkl.HIGHEST_PROTOCOL)


def get_current_datetime():
    return datetime.now().replace(tzinfo=pytz.UTC)
