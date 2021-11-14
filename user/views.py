import os
import pickle as pkl
import random
from datetime import datetime, timedelta

import pandas as pd
import torch
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from beer.models import Beer
from nn.config import Config
from user.models import User, UserBeer
from beer.models import Category
from .util import format_results, \
    load_model, load_last_time_trained, \
    save_last_time_trained, get_current_datetime


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
    global model
    try:
        last_time_trained: datetime = load_last_time_trained()
        now = get_current_datetime()
        minimal_date = last_time_trained + timedelta(days=int(os.getenv('TRAIN_N_DAYS')))
        if now < minimal_date:
            return JsonResponse({'neutral': f'{os.getenv("TRAIN_N_DAYS")} day(s) has not been passed'})

        new_user_ids = []
        new_beer_ids = []
        for user_beer in UserBeer.objects.filter(
                date_added__gte=last_time_trained):
            new_user_ids.append(user_beer.user.id)
            new_beer_ids.append(user_beer.beer.id)

        if len(new_user_ids) <= 0:
            return HttpResponse('No users to train')

        new_user_ratings = [1 for _ in range(len(new_user_ids))]
        new_train_ratings = pd.DataFrame(data=list(zip(new_user_ids, new_beer_ids, new_user_ratings)),
                                         columns=['user_id', 'beer_id', 'rating'])
        pkl.dump(new_train_ratings, open(Config.retrain_data_path, 'wb+'), protocol=pkl.HIGHEST_PROTOCOL)
        os.system(f'python3 nn/train.py -u {os.getenv("NUM_USERS")} -i {os.getenv("NUM_ITEMS")}')

        model = load_model()
        save_last_time_trained(now)

        return JsonResponse({'success': 'The NN has been retrained!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
