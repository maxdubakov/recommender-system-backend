import pandas as pd
from django.http import HttpResponse, JsonResponse

from beer.models import Beer, Category


def get_categories(request):
    categories = []
    for category in Category.objects.all():
        categories.append({"id": category.id, "name": category.name})
    return JsonResponse({"categories": categories})


# DEVELOPMENT ENDPOINTS
data_path = './data/beer_new_reviews.csv'


def save_to_beer(entry):
    beer = Beer(name=entry[0], id=entry[1])
    beer.save()


def save_to_category(entry):
    category = Category(name=entry)
    category.save()


def populate_beers(request):
    data = pd.read_csv(data_path)

    beers: pd.DataFrame = data[['beer_name', 'beer_beerid']].drop_duplicates()
    beers.apply(save_to_beer, axis=1)

    return HttpResponse(f'Done. Posted {len(beers)} beers')


def populate_categories(request):
    data = pd.read_csv(data_path)

    categories = data['beer_style'].drop_duplicates()
    categories.apply(save_to_category)
    return HttpResponse(f'{len(categories)} categories have been saved.')


def delete_categories(request):
    categories = Category.objects.all()
    for c in categories:
        c.delete()
    return HttpResponse('All good')


def populate_beer_to_categories(request):
    data = pd.read_csv(data_path)[['beer_beerid', 'beer_style']]
    categories = Category.objects.all()
    number_of_cat = len(categories)
    for i, category in enumerate(categories):
        beer_ids = list(data['beer_beerid'][data['beer_style'] == category.name].unique())
        print(f'Populating category {category.name} with {len(beer_ids)} beers ({i}/{number_of_cat})')
        for beer_id in beer_ids:
            beer = Beer.objects.get(id=beer_id)
            category.beers.add(beer)

    return HttpResponse(f'All Good')


def delete_beers(request):
    beers = Beer.objects.all()
    for b in beers:
        b.delete()
    return HttpResponse('All good')
