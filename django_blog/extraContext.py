from django_blog.roles import canCreate
from django.core.cache import cache
from django.conf import settings
import requests

def getCachedDeals():
    response = requests.get(f'https://{settings.PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/deals?api_token={settings.PIPEDRIVE_TOKEN}') 
    response = response.json()
    print('deals requestsed')
    deals = []
    i= len(response['data'])-1
    while i >= 0 :
        # if i < 0:
        #     break
        current_deal = {}
        current_deal['id'] = response['data'][i]['id']
        current_deal['handler'] = response['data'][i]['creator_user_id']['name']
        current_deal['title'] = response['data'][i]['title']
        current_deal['price'] = str(response['data'][i]['value'])
        current_deal['status'] = response['data'][i]['status']
        current_deal['currency'] = response['data'][i]['currency']
        current_deal['date_created'] = response['data'][i]['add_time']
        current_deal['last_update'] = response['data'][i]['update_time']
        current_deal['close_time'] = response['data'][i]['close_time']
        current_deal['won_time'] = response['data'][i]['won_time']
        current_deal['lost_time'] = response['data'][i]['lost_time']
        
        deals.append(current_deal)
        i-= 1
    last3Deals = deals[:3]
    cache.set('dealsRequest', deals, 60)
    cache.set('last3Deals', last3Deals, 60)
    return last3Deals,deals

def canCreateNewPost_renderer(request):
    # print(request.META)

    # requested deals
    Rdeals = cache.get('last3Deals')
    if not Rdeals:
        last3Deals, deals = getCachedDeals()
        print(deals)
        Rdeals = last3Deals
    else:
        print('cache stored')

    
    context = {
        'CurrentUserCanPost' : canCreate(request.user),
        'Deals' : Rdeals
    }
    return (context)
