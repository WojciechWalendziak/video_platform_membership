from . import views
from django.urls import path
from .views import RegisterView, ProfileList, ProfileCreate, Watch, ShowMovieDetail, ShowMovie, login_request, logout_request

app_name = 'my_video_platform'

urlpatterns = [
    path('', views.start_view, name='start_view'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('profile/', ProfileList.as_view(), name='profile_list'),
    path('profile_create/', ProfileCreate.as_view(), name='profile_create'),
    path('watch/<str:profile_id>/', Watch.as_view(), name='watch'),
    path('movie_detail/<str:movie_id>/', ShowMovieDetail.as_view(), name='show_det'),
    path('movie/<str:movie_id>/', ShowMovie.as_view(), name='play')
]