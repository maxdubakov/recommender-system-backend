from django.http import HttpResponse

def index(request):
    return HttpResponse('Hey')


def get_beers(request):
    return HttpResponse('Get-beers')


def post_beers(request):
    return HttpResponse('Post-beers')
