from django.urls import path
from . import views as v

urlpatterns = [
    path('',v.apiexpo_index,name="apiexpoindex"),
    path('apicrops/',v.apicrops,name="apicrops"),
    path('apideals/',v.apideals,name="apideals")
]