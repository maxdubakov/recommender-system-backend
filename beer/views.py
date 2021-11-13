from django.http import JsonResponse

from beer.models import Category


def get_categories(request):
    try:
        categories = []
        for category in Category.objects.all():
            categories.append({"id": category.id, "name": category.name})
        return JsonResponse({"categories": categories})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
