from django.db.models import Sum

from src.core.models import Subcategory


def list_subcategories(request):
    categories_obj = Subcategory.objects.filter()
    subcategs = [
        {
            "category_name": categories_obj[0].name,
            "id": categories_obj[0].id,
            "icon": "fa-solid fa-mobile",
            "text_color": "text-first",
            "bg_color": "bg-first"
        },
        {
            "category_name": categories_obj[1].name,
            "id": categories_obj[1].id,
            "icon": "fa-solid fa-clock",
            "text_color": "text-second",
            "bg_color": "bg-second"
        },
        {
            "category_name": categories_obj[2].name,
            "id": categories_obj[2].id,
            "icon": "fa-solid fa-tablet",
            "text_color": "text-third",
            "bg_color": "bg-third"
        },
        {
            "category_name": categories_obj[3].name,
            "id": categories_obj[3].id,
            "icon": "fa-solid fa-coffee",
            "text_color": "text-fourth",
            "bg_color": "bg-fourth"
        },
        {
            "category_name": categories_obj[4].name,
            "id": categories_obj[4].id,
            "icon": "fa-solid fa-tablet",
            "text_color": "text-fifth",
            "bg_color": "bg-fifth"
        },
        {
            "category_name": categories_obj[5].name,
            "id": categories_obj[5].id,
            "icon": "fa-solid fa-tv",
            "text_color": "text-sixth",
            "bg_color": "bg-sixth"
        },
    ]
    return subcategs


def list_popular_subcategories(request):
    popular_subcategories = Subcategory.objects.annotate(
        total_sold=Sum("product__orderitem__quantity")
    ).order_by("-total_sold")[:4]
    return popular_subcategories
