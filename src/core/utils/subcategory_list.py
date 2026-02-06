from src.core.models import Subcategory
from django.db.models import Sum


def list_subcategories(request):
    categories = list(Subcategory.objects.all()[:6])

    meta = [
        ("fa-solid fa-mobile", "text-first", "bg-first"),
        ("fa-solid fa-clock", "text-second", "bg-second"),
        ("fa-solid fa-tablet", "text-third", "bg-third"),
        ("fa-solid fa-coffee", "text-fourth", "bg-fourth"),
        ("fa-solid fa-tablet", "text-fifth", "bg-fifth"),
        ("fa-solid fa-tv", "text-sixth", "bg-sixth"),
    ]

    subcategs = []

    for category, (icon, text, bg) in zip(categories, meta):
        subcategs.append({
            "category_name": category.name,
            "id": category.id,
            "icon": icon,
            "text_color": text,
            "bg_color": bg,
        })

    return subcategs


def list_popular_subcategories(request):
    popular_subcategories = Subcategory.objects.annotate(
        total_sold=Sum("product__orderitem__quantity")
    ).order_by("-total_sold")[:4]
    return popular_subcategories
