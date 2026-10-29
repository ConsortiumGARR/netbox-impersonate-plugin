from django.urls import path
from django.views.decorators.http import require_POST
from impersonate import views

urlpatterns = (
    path("start/<int:uid>/", require_POST(views.impersonate), name="impersonate_start"),
    path("stop/", require_POST(views.stop_impersonate), name="impersonate_stop"),
)
