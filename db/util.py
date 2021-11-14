from beer.models import Beer, Category
from user.models import User, UserBeer


def save_beer(entry):
    beer = Beer(name=entry[0], id=entry[1])
    beer.save()


def save_category(name):
    category = Category(name=name)
    category.save()


def save_user(profile_names_to_id, username):
    user = User(name=username, id=profile_names_to_id[username])
    user.save()


def save_user_beer(entry):
    user = entry[0]
    beer = Beer.objects.get(id=entry[1])
    user_beer = UserBeer(user=user, beer=beer)
    user_beer.save()
