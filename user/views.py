import os
import pickle as pkl
import random

import pandas as pd
import torch
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from beer.models import Beer
from user.models import User
from beer.models import Category
from .util import format_results, load_model

model = load_model()


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
        user_id = int(request.POST['user_id'])
        n = int(request.POST['n'])
        category_ids = [int(_id) for _id in request.POST.getlist('categories')]
        user = User.objects.get(id=user_id)
        beers_for_categories = []
        for cat_id in category_ids:
            category = Category.objects.get(id=cat_id)
            user.categories.add(category)
            all_beers = list(category.beers.all())
            beers = [{'id': beer.id, 'name': beer.name}
                     for beer in random.sample(all_beers, min(len(all_beers), n))]
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
        n = int(request.GET['n'])
        if n < 0:
            return HttpResponse('n is less than 0', status=400)

        user = User.objects.get(id=user_id)

        beer_ids = [beer.id for beer in list(Beer.objects.all())]
        user_tensor = torch.tensor([user_id for _ in range(len(beer_ids))])
        beer_tensor = torch.tensor(beer_ids)

        results = model(user_tensor, beer_tensor).detach().squeeze().tolist()
        results_with_beer_ids = sorted([[b_id, rating] for b_id, rating in zip(beer_ids, results)],
                                       key=lambda _e: 1 - _e[1])[0:n]
        results_with_beers = format_results(results_with_beer_ids)
        return JsonResponse(
            {
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'beers': results_with_beers
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def train(request):
    try:
        new_user_id = [33387 for i in range(5)]
        new_users_beer_ids = [47986, 64883, 33061, 33061, 48213]
        new_user_ratings = [1 for i in range(5)]
        new_train_ratings = pd.DataFrame(data=list(zip(new_user_id, new_users_beer_ids, new_user_ratings)),
                                         columns=['user_id', 'beer_id', 'rating'])
        pkl.dump(new_train_ratings, open('./nn/data/data.pkl', 'wb+'), protocol=pkl.HIGHEST_PROTOCOL)
        os.system('python3 nn/train.py')
        return HttpResponse('All Good!')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
