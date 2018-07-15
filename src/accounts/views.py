import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import BlockProducer, Country

# # Create your views here.


# # In [12]: def get_users():
# #     ...:     count = 1
# #     ...:     for i in range(19):
# #     ...:         r = requests.get('https://api.stackexchange.com/2.2/users?site=eosio&pagesize=100&page={}'.format(count))
# #     ...:         data = json.loads(r.text)
# #     ...:         if data['has_more'] == True:
# #     ...:             for item in data['items']:
# #     ...:                 if item['account_id'] > 0 and item['user_id'] > 0:
# #     ...:                     User.objects.create_user(se_display_name=item['display_name'], username=item['user_id'], se_account_id=item['account_id'], se_user_id=item['user_id'], se_profile_image=item['
# #     ...: profile_image'], se_link=item['link'], se_reputation=item['reputation'], first_name = item['display_name'], last_name=item['display_name'], bronze_badges=item['badge_counts']['bronze'], silver_b
# #     ...: adges=item['badge_counts']['silver'], gold_badges=item['badge_counts']['gold'],password='zxcvbnm,.')
# #     ...:             print('Created')
# #     ...:             count+=1
# #     ...:             print(count)
# #     ...:         else:
# #     ...:             #User.objects.bulk_create(users)
# #     ...:             print(count)
# #     ...:
# #     ...:
# #     ...:
# #     ...:


def home(request):
    return render(request, 'map.html')


def countries(request):
    countries = serialize('geojson', Country.objects.all())
    return HttpResponse(countries, content_type='json') 

# def bps(request):
#     bps = serialize('geojson', BlockProducer.objects.all())
#     return HttpResponse(bps, content_type='json')



def bps(request):
    points_as_geojson = serialize( 'geojson',BlockProducer.objects.all()[:30])
    return JsonResponse(json.loads(points_as_geojson))
