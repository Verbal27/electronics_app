from src.core.models.category import Category


def categories_processor(request):
    return {"categories": Category.objects.prefetch_related("subcategories").all()}
