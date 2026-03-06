from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from src.core.models import Product
from src.core.models.product import ProductReview
from src.website.forms.product_detail import ReviewForm
from src.website.services.moderation import ReviewModerationService
from src.website.services.product_detail_services import ProductDetailService


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        product = self.object
        service = ProductDetailService(self.request, product)
        return service.build_context()


class PostReviewView(LoginRequiredMixin, CreateView):
    model = ProductReview
    form_class = ReviewForm

    def get_success_url(self):
        return reverse("product_detail", args=[self.product.id])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.product = get_object_or_404(Product, pk=self.kwargs["pk"])
        kwargs["user"] = self.request.user
        kwargs["product"] = self.product
        return kwargs

    def form_valid(self, form):
        try:
            self.model.check_cooldown(
                user=self.request.user,
                product=self.product,
            )
        except ValidationError as e:
            messages.error(self.request, e.message)
            return redirect("product_detail", pk=self.product.pk)

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.product = self.product
            self.object.user = self.request.user
            self.object.save()
            ReviewModerationService.moderate(self.object)

            messages.success(self.request, "Review created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong")
        return super().form_invalid(form)


class ReviewsInfiniteScrollView(ListView):
    model = ProductReview
    paginate_by = 5
    template_name = "partials/reviews_list.html"

    def get_queryset(self):
        self.product = get_object_or_404(
            Product,
            pk=self.kwargs["pk"]
        )

        return (
            self.product.reviews
                .select_related("user")
                .with_verified_purchase()
                .order_by("-created_at")
        )

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string(
            self.template_name,
            {"reviews": context["page_obj"]},
            request=self.request,
        )

        return JsonResponse({
            "html": html,
            "has_next": context["page_obj"].has_next(),
        })
