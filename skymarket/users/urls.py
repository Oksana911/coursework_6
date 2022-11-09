from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views

users_router = SimpleRouter()

users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(users_router.urls)),
    path("api/token/", views.TokenObtainPairView.as_view()),
    path("refresh/", views.TokenRefreshView.as_view()),
]
