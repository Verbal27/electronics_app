from src.users.forms.account_info import ProfileImageChange


class CabinetContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_image"] = ProfileImageChange(
            instance=self.request.user
        )
        return context
