from django.db.models import Count
from django.core.cache import cache
from kino.models import *

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "О сайте", 'url_name': 'about'},
]

class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('movie'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context