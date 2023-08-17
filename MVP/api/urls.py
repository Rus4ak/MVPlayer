from django.urls import path, include
from .views import SongList, SongDetail, UserList, UserDetail


urlpatterns = [
    path('', SongList.as_view()),
    path('<int:pk>/', SongDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
