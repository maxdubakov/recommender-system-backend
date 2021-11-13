import pickle as pkl

import torch

from beer.models import Beer
from user.models import User
from nn.NCF import NCF


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
    model = NCF(33388, 77318, [], all_beer_ids())
    model.load_state_dict(torch.load('./nn/models/model_dict.pt'))
    model.eval()
    return model
