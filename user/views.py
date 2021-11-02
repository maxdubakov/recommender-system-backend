import pickle as pkl

from django.http import HttpResponse
import pandas as pd

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
    return HttpResponse('All Good')
