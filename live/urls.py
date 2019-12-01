from django.urls import path, re_path

from live import views

app_name = "live"

urlpatterns = [
    re_path(
        r"^(?P<feature_slug>(?!ws|guest|supervise)[^/^]+)/$",
        views.guest_welcome,
        name="index",
    ),
    path("guest/interact/", views.guest_interact, name="guest_interact"),
    path("supervise/", views.supervise, name="supervise"),
    path("guest/exit/", views.guest_exit, name="guest_exit"),
]
