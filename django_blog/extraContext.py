from django_blog.roles import canCreate
from django.core.cache import cache
from django.conf import settings
import requests

def canCreateNewPost_renderer(request):
    # print(request.META)

   
    Rdeals = cache.get('dealsRequest')
    if not Rdeals:
        response = requests.get(f'https://kf.pipedrive.com/api/v1/deals?api_token={settings.PIPEDRIVE_TOKEN}') 
        response = response.json()
        print('deals requestsed')
        deals = []
        i= len(response['data'])-1
        while i > (len(response['data']) -4 ):
            if i < 0:
                break
            current_deal = {}
            current_deal['id'] = response['data'][i]['id']
            current_deal['title'] = response['data'][i]['title']
            current_deal['cost'] = str(response['data'][i]['value'])+ ' ' + response['data'][i]['currency']
            current_deal['status'] = response['data'][i]['status']
            deals.append(current_deal)
            i-= 1
        print(deals)
        Rdeals = deals
        cache.set('dealsRequest', deals, 30)
    else:
        print('cache stored')

    
    context = {
        'CurrentUserCanPost' : canCreate(request.user),
        'Deals' : Rdeals
    }
    return (context)
