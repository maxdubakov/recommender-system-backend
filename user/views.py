import pickle as pkl

from django.http import HttpResponse
import pandas as pd

from beer.models import Beer
from user.models import User

data_path = './data/beer_new_reviews.csv'

def index(request):
    return HttpResponse('Index Page')


def save_user(profile_names_to_id, username):
    user = User(name=username, id=profile_names_to_id[username])
    user.save()


def populate_users(request):
    data = pd.read_csv(data_path)
    profile_names_to_id = pkl.load(open('./data/review_profilename_to_user_id.pkl', 'rb'))
    users = data['review_profilename'].drop_duplicates().dropna()
    users.apply(lambda username: save_user(profile_names_to_id, username))
    return HttpResponse('All Good')

def populate_users_beers(request):
    data = pd.read_csv(data_path)

    users = User.objects.all()
    number_of_users = len(users)
    for i, user in enumerate(users):
        if i >= 100:
            break
        beer_ids = list(data['beer_beerid'][data['review_profilename'] == user.name].unique())
        print(f'Populating {len(beer_ids)} beers for user {user} ({i}/{number_of_users})')
        for beer_id in beer_ids:
            beer = Beer.objects.get(id=beer_id)
            user.beers.add(beer)

    return HttpResponse('All Good')


def get_beers_for_user(request, slug):
    user = User.objects.get(name=slug)
    return HttpResponse(f'All Good:\n {[beer.name for beer in user.beers.all()]}\n\n{user.name}\n\n {len(user.beers.all())}')
