from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("exc_library/", views.exc_library, name="exc_library"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("saved_exc",views.saved_exercise,name="saved_exc"),
    path("filter_exercises/",views.filter_exercises,name="filter_exercises"),
    path("filtered_exercises/",views.filtered_exercises,name="filtered_exercises"),
    path("save_exercise/<int:id>",views.save_exercise,name="save_exercise"),
    path("unsave_exercise/<int:id>",views.unsave_exercise,name="unsave_exercise"),
    path("results",views.results,name="results"),
    path("progress/",views.progress,name="progress"),
    path("complete_exercise/<int:id>/",views.complete_exercise,name="complete_exercise"),
]