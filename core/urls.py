from django.urls import path
from core.views import index

app_name = "core"

#indicate the url patterns
urlpatterns = [
    path("", index, name="index")
]