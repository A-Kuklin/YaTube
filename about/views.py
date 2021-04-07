from django.views.generic.base import TemplateView


class AuthorPage(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context["title"] = "Об авторе проекта"
        context["short_title"] = "Об авторе"
        context["short_story"] = "42"
        context["long_story"] = "Don't panic"
        return context


class TechPage(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context["title"] = "О технологиях проекта"
        context["short_title"] = "О технологиях"
        context["short_story"] = "ЯП"
        context["long_story"] = "Google"
        return context
