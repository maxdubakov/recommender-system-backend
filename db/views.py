import os
import pickle as pkl
import time

from django.http import HttpResponse, JsonResponse
import pandas as pd

from beer.models import Beer, Category
from user.models import User, UserBeer
from .util import save_beer, save_category, save_user, save_user_beer


def populate_all(request):
    try:
        start_time = time.time()

        if len(User.objects.all()) > 0:
            return HttpResponse('Already populated', status=400)

        data = pd.read_csv(os.getenv('DATA_PATH'))
        beers = populate_beers(data)
        users = populate_users(data)
        categories = populate_categories(data)
        user_beers = populate_user_beers(data)
        category_beers = populate_category_beers(data)

        end_time = time.time()

        return JsonResponse({
            'beers': beers,
            'users': users,
            'categories': categories,
            'user_beers': user_beers,
            'category_beers': category_beers,
            'time': f'{str(end_time - start_time)}s'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})


def populate_beers(data):
    print('Populating Beer table...')
    beers: pd.DataFrame = data[['beer_name', 'beer_beerid']].drop_duplicates()
    beers.apply(save_beer, axis=1)
    return len(Beer.objects.all())


def populate_users(data):
    print('Populating User table...')
    profile_names_to_id = pkl.load(open('./data/review_profilename_to_user_id.pkl', 'rb'))
    users = data['review_profilename'].drop_duplicates().dropna()[1000:]
    users.apply(lambda username: save_user(profile_names_to_id, username))
    return len(User.objects.all())


def populate_categories(data):
    print('Populating Catetory table...')
    categories = data['beer_style'].drop_duplicates()
    categories.apply(save_category)
    return len(Category.objects.all())


def populate_user_beers(data):
    print('Populating UserBeer table...')
    users = User.objects.all()
    number_of_users = len(users)
    for i, user in enumerate(users):
        beer_ids = list(data['beer_beerid'][data['review_profilename'] == user.name].unique())
        print(f'Populating {len(beer_ids)} beers for user {user} ({i}/{number_of_users})')
        for beer_id in beer_ids:
            save_user_beer([user, beer_id])
    return len(UserBeer.objects.all())


def populate_category_beers(data):
    print('Populating CategoryBeer table...')
    data = data[['beer_beerid', 'beer_style']]
    categories = Category.objects.all()
    number_of_cat = len(categories)
    c = 0

    for i, category in enumerate(categories):
        beer_ids = list(data['beer_beerid'][data['beer_style'] == category.name].unique())
        print(f'Populating category {category.name} with {len(beer_ids)} beers ({i}/{number_of_cat})')
        for beer_id in beer_ids:
            beer = Beer.objects.get(id=beer_id)
            category.beers.add(beer)
            c += 1
    return c
