
from src.core.models.category import Category
from src.website.forms import UserLogoutForm


def categories_processor(request):
    return {"categories": Category.objects.prefetch_related("subcategories").all()}


def logout(request):
    return {"logout_form": UserLogoutForm()}