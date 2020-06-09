from django.views.generic.base import View, TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class NotFoundView(TemplateView):
    template_name = '404.html'


class AddlistingView(TemplateView):
    template_name = 'addlisting.html'


class Addlisting2View(TemplateView):
    template_name = 'addlisting2.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class BlogSingleView(TemplateView):
    template_name = 'blog-single.html'


class ComingsoonView(TemplateView):
    template_name = 'comingsoon.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class ExploreDetailView(TemplateView):
    template_name = 'explore-detail.html'


class ExploreV1View(TemplateView):
    template_name = 'explore-v1.html'


class ExploreV2View(TemplateView):
    template_name = 'explore-v2.html'


class ExploreV3View(TemplateView):
    template_name = 'explore-v3.html'


class ExploreV4View(TemplateView):
    template_name = 'explore-v4.html'


class ExploreV5View(TemplateView):
    template_name = 'explore-v5.html'


class Index2View(TemplateView):
    template_name = 'index2.html'


class IndexCopyView(TemplateView):
    template_name = 'index拷貝.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class PriceView(TemplateView):
    template_name = 'price.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
