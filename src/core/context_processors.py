
from src.core.models.category import Category
from src.website.forms import UserLogoutForm
from src.website.forms.newsletter import NewsletterForm
from src.website.forms.search import Search


def categories_processor(request):
    return {"categories": Category.objects.prefetch_related("subcategories").all()}


def logout(request):
    return {"logout_form": UserLogoutForm()}


def cart_count(request):
    cart = request.session.get("cart", {})

    total_qty = 0
    for item in cart.values():
        if isinstance(item, dict):
            total_qty += item.get("quantity", 0)
        else:
            total_qty += int(item)

    return {"cart_count": total_qty}


def search_bar(request):
    return {"search": Search()}


def newsletter(request):
    return {"newsletter": NewsletterForm()}
