from django.views.decorators.csrf import csrf_exempt

from .views import *


from django.urls import path

urlpatterns = [
    path('login/', csrf_exempt(LoginView.as_view())),
    path('logout/', csrf_exempt(LogoutView.as_view())),
    path('register/', csrf_exempt(RegisterView.as_view())),
    path('upload/', csrf_exempt(MusicView.as_view())),
    path('upload/<str:title>/', csrf_exempt(MusicView.as_view())),
    path('musics/', csrf_exempt(SearchView.as_view())),
    path('rating/<str:title>', csrf_exempt(RatingView.as_view())),
    path('rating/', csrf_exempt(RatingView.as_view()))
]
