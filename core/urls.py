from django.urls import path
from core.views import index

app_name = "urls"

#indicate the url patterns
urlpatterns = [
    path("", index)
]