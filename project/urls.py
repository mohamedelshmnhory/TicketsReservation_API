"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.ViewSetsGuest)
router.register('movies', views.ViewSetsMovie)
router.register('reservations', views.ViewSetsReservation)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 1
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    # 2
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),

    # 3.1 GET POST from rest framework function based view @api_view
    path('rest/fbv/', views.fbv_list),

    # 3.2 GET PUT DELETE rest framework function based view @api_view
    path('rest/fbv/<int:pk>', views.fbv_pk),

    # 4.1 GET POST from rest framework class based view APIView
    path('rest/cbv/', views.CBVList.as_view()),

    # 4.2 GET PUT DELETE from rest framework class based view APIView
    path('rest/cbv/<int:pk>', views.CBVpk.as_view()),

    # 5.1 GET POST from rest framework class based view mixins
    path('rest/mixins/', views.MixinsList.as_view()),

    # 5.2 GET PUT DELETE from rest framework class based view mixins
    path('rest/mixins/<int:pk>', views.MixinsPk.as_view()),

    # 6.1 GET POST from rest framework class based view generics
    path('rest/generics/', views.GenericsList.as_view()),

    # 6.2 GET PUT DELETE from rest framework class based view generics
    path('rest/generics/<int:pk>', views.GenericsPk.as_view()),

    # 7 ViewSets
    path('rest/viewsets/', include(router.urls)),

    # 8 find movie
    path('fbv/findmovie/', views.find_movie),

    # 9 new reservation
    path('fbv/newreservation/', views.new_reservation),

    # 10 rest auth url
    path('api-auth', include('rest_framework.urls')),

    # 11 token authentication
    path('api-token-auth', obtain_auth_token),

    # 12 Post pk generics Post_pk
    # path('post/generics/', views.PostList.as_view()),
    path('post/generics/<int:pk>', views.PostPk.as_view()),
]
