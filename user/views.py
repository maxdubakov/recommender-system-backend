import pickle as pkl
import random

import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from beer.models import Beer
from user.models import User
from beer.models import Category

data_path = './data/beer_new_reviews.csv'

@csrf_exempt
def post_user(request):
    try:
        name = request.POST['name']
        _id = int(User.objects.all().aggregate(Max('id'))['id__max']) + 1
        new_user = User(id=_id, name=name)
        new_user.save()
        return JsonResponse({
            "id": _id,
            "name": name
        })
    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
def post_user_categories(request):
    try:
        user_id = int(request.POST["user_id"])
        category_ids = [int(_id) for _id in request.POST.getlist('categories')]
        user = User.objects.get(id=user_id)
        beers_for_categories = []
        for cat_id in category_ids:
            category = Category.objects.get(id=cat_id)
            user.categories.add(category)
            all_beers = list(category.beers.all())
            if len(all_beers) >= 5:
                beers = [{'id': beer.id, 'name': beer.name} for beer in random.sample(all_beers, 5)]
                beers_for_categories.append({category.name: beers})
        return JsonResponse({'categories': beers_for_categories})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def post_user_beers(request):
    try:
        user_id = request.POST['user_id']
        beer_ids = [int(_id) for _id in request.POST.getlist('beers')]
        user = User.objects.get(id=user_id)
        for beer_id in beer_ids:
            beer = Beer.objects.get(id=beer_id)
            user.beers.add(beer)
        return HttpResponse()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_user_beers(request):
    try:
        user_id = int(request.GET['user_id'])
        user = User.objects.get(id=user_id)
        beers = user.beers.all()
        list_beers = []
        for beer in beers:
            list_beers.append({'id': beer.id, 'name': beer.name})
        return JsonResponse({
            'user_id': user.id,
            'user_name': user.name,
            'beers': list_beers
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def predict_beers(request):
    try:
        user_id = int(request.GET['user_id'])
        user = User.objects.get(id=user_id)
        beers = [{'id': beer.id, 'name': beer.name} for beer in random.sample(list(Beer.objects.all()), 20)]
        return JsonResponse({'user': {'id': user.id, 'name': user.name} ,'beers': beers})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# DEVELOPMENT ENDPOINTS
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
