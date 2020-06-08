from django.views.generic.base import View, TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
