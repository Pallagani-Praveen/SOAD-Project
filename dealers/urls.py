from django.urls import path,include
from . import views as v
urlpatterns = [
    path('',v.dealer_index,name="dealer_index"),
    path('all_crops',v.get_all_crops,name='get_all_crops'),
    path('crop_eval',v.crop_eval,name='crop_eval'),
    path('add_deal',v.add_deal,name="add_crop"),
    path('profile',v.dealer_profile,name="dealer_profile"),
    path('deal_details',v.deal_details,name="deal_details"),
    path('deal_status',v.deal_status,name="deal_status"),
    path('requests',v.dealer_requests,name="dealer_requests"),
    path('delete',v.delete,name="delete"),

    # ajax urls
    path('request',v.makeRequestResponse,name="requestresponse"),
    path('sendrequest',v.makeRequest,name="makerequest"),
]