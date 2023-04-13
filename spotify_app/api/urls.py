from django.urls import path, include

urlpatterns = [
    path('users/', include('spotify_app.authentication.urls'))
]
