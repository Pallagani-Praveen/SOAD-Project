from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from bson.objectid import ObjectId
from numpy import std,mean
from farmers.models import PinToLatLong
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auths.models import User
from statistics import mean,stdev

client = MongoClient().getConnection()

# Create your views here.
@login_required(login_url='/auth/login')
def dealer_index(request):
    deals = list(client.Farmify.dealers_deals.find({'user':request.user.email}))
    farmer_requested_deals = list(client.Farmify.farmer_request_dealer.find({'dealer':request.user.email}))
    for deal in deals:
        deal['timestamp'] = deal['_id'].generation_time
        deal['id'] = deal['_id']
        temp_reqs = []
        for farmer_req in farmer_requested_deals:
            if ObjectId(farmer_req['deal_id']) == deal['_id']:
                temp_reqs.append(farmer_req)
        deal['readyfarmers'] = len(temp_reqs)
    context = {'deals':deals}
    return render(request,'dealers/dealer_index.html',context=context)

@login_required(login_url='/auth/login')
def add_deal(request):
    if request.user.role == 'farmer':
        messages.warning(request,'Action Not Allowed')
        return redirect('/')

    if request.method == 'POST':
        cropname = request.POST['cropname']
        start_size = request.POST['start_size']
        end_size = request.POST['end_size']
        metric = request.POST['metric']
        price = request.POST['price']

        state = request.POST['state']
        pincode = request.POST['pincode']
        area = request.POST['area']
        phone = request.POST['phone']

        doc = dict()
        doc['user'] = request.user.email
        doc['cropname'] = cropname
        doc['start_size'] = start_size
        doc['end_size'] = end_size
        doc['metric'] = metric
        doc['price'] = price
        doc['state'] = state
        doc['pincode'] = pincode
        doc['area'] = area
        doc['phone'] = phone

        client.Farmify.dealers_deals.insert(doc)
        return redirect('/dealers/')

    return render(request,'dealers/add_deal.html')


def get_all_crops(request):
    crops = list(client.Farmify.farmers_crops.find())
    for crop in crops:
        crop['id'] = crop['_id']
        crop['timestamp'] = crop['_id'].generation_time
        crop['readydealers'] = len(list(client.Farmify.dealer_request_farmer.find({'crop_id':str(crop['id'])})))
    context = {'crops':crops}
    return render(request,'dealers/all_crops.html',context=context)

@login_required(login_url='/auth/login')
def crop_eval(request):
    def eval_per_unit_price(crop):
        return int(crop['price'])/int(crop['size'])
    if 'crop_id' not in request.GET:
        return redirect('/')

    cropid = request.GET['crop_id']
    crop = list(client.Farmify.farmers_crops.find({'_id':ObjectId(cropid)}))[0]
    crop['id'] = crop['_id']
    print(str(crop['id']))
    crops = list(client.Farmify.farmers_crops.find({'cropname':crop['cropname']}))
    is_req_crop = list(client.Farmify.dealer_request_farmer.find({'crop_id':str(crop['id']),'dealer':request.user.email}))
    if is_req_crop:
        is_req_crop = is_req_crop[0]
    print(is_req_crop)
    per_unit_prices = list(map(eval_per_unit_price,crops))
    mu,sd = mean(per_unit_prices),std(per_unit_prices)

    if mu-sd <= eval_per_unit_price(crop) <= mu+sd:
        color = 'success'
        sugg = 'Go'
    elif (mu-2*sd) <= eval_per_unit_price(crop) <= (mu+2*sd):
        color = 'primary'
        sugg = 'Think'
    else:
        color = 'danger'
        sugg = 'No'

    if PinToLatLong.objects.filter(pin=int(crop['pincode'])).count()!=0:
        pintolatlong = PinToLatLong.objects.filter(pin=int(crop['pincode']))[:1].get()
        lat = pintolatlong.lat
        long = pintolatlong.long
        area = crop['area']
    else:
        lat = 18.4435
        long = 83.546
        area = 'Undetermined'

    context = {'crop':crop,'crops':crops,'mu':mu,'sd':sd,'cropname':crop['cropname'],'color':color,'sugg':sugg,'lat':lat,'long':long,'area':area,'is_req_crop':is_req_crop}
    return render(request,'dealers/crop_eval.html',context=context)

@login_required(login_url='/auth/login')
def dealer_profile(request):
    user = request.user
    context = {'user':user}
    return render(request,'dealers/dealer_profile.html',context=context)

@login_required(login_url='/auth/login')
def deal_details(request):
    if 'deal_id' not in request.GET:
        messages.warning(request,'Action Not Allowed')
        return redirect('/')

    deal_id = request.GET['deal_id']
    farmers = list(client.Farmify.farmer_request_dealer.find({'deal_id':deal_id}))
    deal = list(client.Farmify.dealers_deals.find({'_id':ObjectId(deal_id)}))[0]
    deal['id'] = deal['_id']
    all_deal_crops = list(client.Farmify.farmers_crops.find({'cropname':deal['cropname']}))
    prices = list(map(lambda x: int(x['price'])/int(x['size']),all_deal_crops))
    if len(prices)<=1:
        context = {'deal':deal,'farmers':farmers,'no_stats':True}
    else:
        mu,sd = mean(prices),stdev(prices) 
        deal_price_range = {'start':int(deal['price'])/int(deal['end_size']),'end':int(deal['price'])/int(deal['start_size'])}
        context = {'deal':deal,'farmers':farmers,'mu':mu,'sd':sd,'deal_price_range':deal_price_range}
    return render(request,'dealers/deal_details.html',context=context)


@login_required(login_url='/auth/login')
def deal_status(request):
    if request.user.role == 'farmer':
        return redirect('/')
    deal_id = request.GET['deal_id']
    deal = list(client.Farmify.farmer_request_dealer.find({'deal_id':deal_id}))[0]
    deal['id'] = deal['_id']
    farmer_crops = list(client.Farmify.farmers_crops.find({'user':deal['farmer']}))
    for farmer_crop in farmer_crops:
        farmer_crop['id'] = farmer_crop['_id']
    context = {'deal':deal,'farmer_crops':farmer_crops}
    return render(request,'dealers/deal_status.html',context=context)

@login_required(login_url='/auth/login')
def dealer_requests(request):
    if request.user.role == 'farmer':
        return redirect('/')
    req_crops = list(client.Farmify.dealer_request_farmer.find({'dealer':request.user.email}))
    all_crops = []
    
    for crop in req_crops:
        c = list(client.Farmify.farmers_crops.find({'_id':ObjectId(crop['crop_id'])}))[0]
        c['status'] = crop['status']
        c['id'] = c['_id']
        all_crops.append(c)
    print(all_crops)
    context = {'req_crops':req_crops,'all_crops':all_crops}
    return render(request,'dealers/dealer_requests.html',context=context)

@login_required(login_url='/auth/login')
def delete(request):
    if 'deal_id' not in request.GET:
        return redirect('/')
    deal_id = request.GET['deal_id']
    print(deal_id)
    res = client.Farmify.dealers_deals.remove({"_id":ObjectId(deal_id)})
    print(res)
    return redirect('/dealers/')

# all ajax requests
def makeRequestResponse(request):
    if request.method == 'POST':
        status = request.POST['status']
        dealid = request.POST['dealid']
        print(dealid,status)
        deal = list(client.Farmify.farmer_request_dealer.find({'deal_id':dealid}))[0]
        client.Farmify.farmer_request_dealer.remove({'deal_id':dealid})
        res = client.Farmify.farmer_request_dealer.insert({'farmer':deal['farmer'],'dealer':deal['dealer'],'deal_id':dealid,'status':status})        
        return HttpResponse(res)
    else:
        return redirect('/')

@login_required(login_url='/auth/login')
def makeRequest(request):
    if request.user.role == 'farmer':
        return redirect('/')

    if request.method=="POST":
        crop_id = request.POST['crop_id']
        farmer = request.POST['farmer']
        dealer = request.POST['dealer']
        res = client.Farmify.dealer_request_farmer.insert({'dealer':dealer,'crop_id':crop_id,'farmer':farmer,'status':'waiting'})
        return HttpResponse(res)
    else:
        return redirect('/')


    
