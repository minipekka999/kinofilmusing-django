from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns =[
    path('', MovieHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='loginn'),
    path('logout/', logout_user, name='logoutt'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/',ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', MovieCategory.as_view(), name='category'),
]