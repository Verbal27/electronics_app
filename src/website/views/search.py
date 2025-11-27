from django.views.generic import ListView

from src.core.models import Product
from src.website.forms.search import Search


class SearchListView(ListView):
    form_class = Search

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            res = list(Product.objects.filter(name__icontains=query))
            return res
        return Product.objects.none()
