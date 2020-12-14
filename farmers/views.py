from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from django.contrib import messages
from bson.objectid import ObjectId
from auths.models import User



client = MongoClient().getConnection()


# Create your views here.

def farmer_index(request):
    crops = list(client.Farmify.farmers_crops.find({'user':request.user.email}))
    for crop in crops:
        crop['timestamp'] = crop['_id'].generation_time
        crop['id'] = crop['_id']
        crop['readydealers'] = len(list(client.Farmify.dealer_request_farmer.find({'crop_id':str(crop['id'])})))
       
    context = {'crops':crops}
    return render(request,'farmers/farmer_index.html',context=context)

@login_required(login_url='/auth/login')
def add_crop(request):
    if request.user.role == 'dealer':
        messages.warning(request,'Action Not Allowed')
        return redirect('/')
    if request.method == 'POST':
        cropname = request.POST['cropname']
        size = request.POST['size']
        metric = request.POST['metric']
        price = request.POST['price']

        state = request.POST['state']
        pincode = request.POST['pincode']
        area = request.POST['area']
        phone = request.POST['phone']

        doc = dict()
        doc['user'] = request.user.email
        doc['cropname'] = cropname
        doc['size'] = size
        doc['metric'] = metric
        doc['price'] = price
        doc['state'] = state
        doc['pincode'] = pincode
        doc['area'] = area
        doc['phone'] = phone

        client.Farmify.farmers_crops.insert(doc)
        return redirect('/farmers/')
    return render(request,'farmers/add_crop.html',context={})

@login_required(login_url='/auth/login')
def related_crop(request,cropname):
    user_crops = list(client.Farmify.farmers_crops.find({'user':request.user.email,'cropname':cropname}))
    
    related_crops = list(client.Farmify.farmers_crops.find({'cropname':cropname,'user':{'$not':{'$regex':request.user.email}}}))
    req_dealers = list(client.Farmify.dealer_request_farmer.find({'crop_id':str(user_crops[0]['_id'])}))
    
    for crop in related_crops:
        crop['timestamp'] = crop['_id'].generation_time
    return render(request,'farmers/related_crops.html',context={'user_crops':user_crops,'cropname':cropname,'related_crops':related_crops,'req_dealers':req_dealers})

@login_required(login_url='/auth/login')
def get_all_deals(request):

    if client==None:
        return redirect('/')

    deals = list(client.Farmify.dealers_deals.find({}))
    farmer_requested_dealer_deals = list(client.Farmify.farmer_request_dealer.find({"farmer":request.user.email}))
    
    for deal in deals:
        deal['img'] = User.objects.get(email=deal['user']).avatar
        deal['timestamp'] = deal['_id'].generation_time
        deal['id'] = deal['_id']
        deal['status'] = 'request'
        for request_deal in farmer_requested_dealer_deals:
            if deal['id'] == ObjectId(request_deal['deal_id']):
                deal['status'] = request_deal['status']
        
        
    context = {'deals':deals}
    return render(request,'farmers/all_deals.html',context=context)


@login_required(login_url='/auth/login')
def farmer_requests(request):
    reqs = list(client.Farmify.farmer_request_dealer.find({'farmer':request.user.email}))
    reqs_details = []
    for req in reqs:
        dts = list(client.Farmify.dealers_deals.find({'_id':ObjectId(req['deal_id'])}))[0]
        dts['status'] = req['status']
        dts['id'] = req['deal_id']
        reqs_details.append(dts)
    context = {'reqs_details':reqs_details}
    return render(request,'farmers/farmer_requests.html',context=context)

def farmer_profile(request):
    user = request.user
    context = {'user':user}
    return render(request,'farmers/farmer_profile.html',context=context)

@login_required(login_url='/auth/login')
def makeRequestResponse(request):
    crop_id = request.GET['crop_id']
    crop_req = list(client.Farmify.dealer_request_farmer.find({'farmer':request.user.email,'crop_id':crop_id}))[0]
    crop_req['id'] = crop_req['_id']
    all_dealer_deals = list(client.Farmify.dealers_deals.find({'user':crop_req['dealer']}))
    for dealer_deal in all_dealer_deals:
        dealer_deal['id'] = dealer_deal['_id']
    context = {'crop_req':crop_req,'all_dealer_deals':all_dealer_deals}
    return render(request,'farmers/crop_status.html',context=context)

# Ajax Working Views
# ---------------------
@login_required(login_url='/auth/login')
def request_dealer_deal(request):
    if request.method == 'POST':
        farmer = request.POST['farmer']
        dealer = request.POST['dealer']
        deal_id = request.POST['deal_id']
        status = 'waiting'
        doc = dict()
        doc['farmer'] = farmer
        doc['dealer'] = dealer
        doc['deal_id'] = deal_id
        doc['status'] = status
        res = client.Farmify.farmer_request_dealer.insert(doc)
        print(type(ObjectId))
        if type(res)==type(ObjectId(res)):
            return HttpResponse('success')
        else:
            return HttpResponse('Error')
    return redirect('/')

@login_required(login_url='/auth/login')
def makeResponse(request):
    if request.method=='POST':
        crop_id = request.POST['crop_id']
        dealer = request.POST['dealer']
        farmer = request.POST['farmer']
        status = request.POST['status']
        client.Farmify.dealer_request_farmer.remove({'farmer':farmer,'crop_id':crop_id})
        res = client.Farmify.dealer_request_farmer.insert({'dealer':dealer,'crop_id':crop_id,'farmer':farmer,'status':status})
        return HttpResponse(res)
    else:
        return redirect('/')

@login_required(login_url='/auth/login')
def delete(request):
    if 'crop_id' not in request.GET:
        return redirect('/')
    crop_id = request.GET['crop_id']
    res = client.Farmify.farmers_crops.remove({"_id":ObjectId(crop_id)})
    return redirect('/farmers/')










