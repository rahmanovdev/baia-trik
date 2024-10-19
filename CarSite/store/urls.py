from django.urls import path
from .views import *

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('user/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_list'),
    path('user/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve',
                                                       'put': 'update', 'delete': 'destroy'}), name='user_detail'),

    path('', CarListViewSet.as_view({'get': 'list', 'post': 'create'}), name='car_list'),
    path('<int:pk>/', CarDetailViewSet.as_view({'get': 'retrieve',
                                                  'put': 'update', 'delete': 'destroy'}), name='car_detail'),

    path('rating', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating_list'),
    path('rating/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve',
                                                   'put': 'update', 'delete': 'destroy'}), name='rating_detail'),

    path('favorite', FavoriteCarViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_list'),
    path('favorite/<int:pk>/', FavoriteCarViewSet.as_view({'get': 'retrieve',
                                                    'put': 'update', 'delete': 'destroy'}), name='favorite_detail'),

    path('favorite_car', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_car_list'),
    path('favorite_car/<int:pk>/', FavoriteViewSet.as_view({'get': 'retrieve',
                                                           'put': 'update', 'delete': 'destroy'}),name='favorite_car_detail'),

    path('history', HistoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='historylist'),
    path('history/<int:pk>/', HistoryViewSet.as_view({'get': 'retrieve',
                                                    'put': 'update', 'delete': 'destroy'}), name='history_detail'),

]

