from django.shortcuts import render,HttpResponse
from farmify.mongoClient import MongoClient
from django.http import JsonResponse
import json
# Create your views here.

client = MongoClient().getConnection()

def apiexpo_index(request):
    return HttpResponse('Api Expo Index Page')

def apicrops(request):
    farmers = list(client.Farmify.farmers_crops.find({}))
    for farmer in farmers:
        farmer['_id'] = str(farmer['_id'])
    response = dict()
    response['name'] = 'allcrops@farmify'
    response['objects_count'] = len(farmers)
    response['data'] = farmers
    return HttpResponse(json.dumps(response),content_type="application/json")

def apideals(request):
    deals = list(client.Farmify.dealers_deals.find({}))
    for deal in deals:
        deal['_id'] = str(deal['_id'])
    response = dict()
    response['name'] = 'alldeals@farmify'
    response['objects_count'] = len(deals)
    response['data'] = deals
    return HttpResponse(json.dumps(response),content_type="application/json")
