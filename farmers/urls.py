from dealers.views import delete
from django.urls import path
from . import views as v
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',v.farmer_index,name="farmer_index"),
    path('add_crop/',v.add_crop,name='add_crop'),
    path('requests/',v.farmer_requests,name='farmer_requests'),
    path('crop/<str:cropname>',v.related_crop,name='related_crop'),
    path('all_deals',v.get_all_deals,name="all_deals"),
    path('request_dealer_deal',v.request_dealer_deal,name="request_dealer_deal"),
    path('request',v.makeRequestResponse,name="makerequestresponse"),
    path('profile',v.farmer_profile,name="farmerprofile"),
    path('delete',v.delete,name="delete"),

    # ajax urls
    path('response',v.makeResponse,name="makeresponse")
] +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
