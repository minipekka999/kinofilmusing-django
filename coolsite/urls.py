"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from coolsite import settings
from kino.views import *
from rest_framework import routers



# class MyCustomRouter(routers.SimpleRouter):
#     routers = [
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get':'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'List'}),
#         routers.Route(url=r'^{prefix}/{lookup}$',
#                       mapping={'get':'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix':'Detail'})
#     ]
#
# router = MyCustomRouter()
# router.register(r'movie', MovieViewSet, basename='movie')
# print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('kino.urls')),
    path('api/v1/movie/', MovieAPIList.as_view()),
    path('api/v1/movie/<int:pk>/', MovieAPIUpdate.as_view()),
    path('api/v1/moviedelete/<int:pk>/', MovieAPIDestroy.as_view()),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(),name='token_obtain.pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(),name='token_verify'),
    # path('api/v1/', include(router.urls))
    # path('api/v1/movielist/', MovieViewSet.as_view({'get':'list'})),
    # path('api/v1/movielist/<int:pk>/',MovieViewSet.as_view({'put':'update'})),
    # path('api/v1/moviedetail/<int:pk>/',MovieAPIDetailView.as_view()),
]
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = pageNotFound