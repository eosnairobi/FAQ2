# import copy  # Copies instances of Image
# import cStringIO  # Used to imitate reading from byte file
# import imghdr  # Used to validate images
import json
import re
# import urllib2  # Used to download images
# import urlparse  # Cleans up image urls
from os.path import basename
from tempfile import TemporaryFile
from urllib.parse import urlsplit

import requests
# from PIL import Image  # Holds downloaded image and verifies it

from django.contrib.gis import geos
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

from .models import BlockProducer, BlockProducerData, User
from celery import shared_task


@shared_task
def get_users():
    count = 1
    for i in range(19):
        r = requests.get(
            'https://api.stackexchange.com/2.2/users?site=eosio&pagesize=100&page={}'.format(count))
        data = json.loads(r.text)
        if data['has_more'] == True:
            for item in data['items']:
                if item['account_id'] > 0 and item['user_id'] > 0:
                    User.objects.create_user(se_display_name=item['display_name'],
                                             username=item['user_id'], se_account_id=item['account_id'],
                                             se_user_id=item['user_id'], se_profile_image=item['profile_image'],
                                             se_link=item['link'], se_reputation=item['reputation'],
                                             first_name=item['display_name'], last_name=item['display_name'],
                                             bronze_badges=item['badge_counts']['bronze'],
                                             silver_badges=item['badge_counts']['silver'],
                                             gold_badges=item['badge_counts']['gold'], password='zxcvbnm,.')
                print('Created')
                count += 1
            else:
                pass


"""
    Structure of BP.JSON
    {
    "producer_account_name":"eosnationftw",
    "producer_public_key":"EOS8PkNNBYU1xnbcjBUNm1mT6N68QiGvCDgPT97rqurLBEjDanSXK",
    "org":{
        "candidate_name":"EOS Nation",
        "website":"https://eosnation.io",
        "ownership_disclosure":"https://eosnation.io#core-team",
        "code_of_conduct":"https://steemit.com/eos/@eosnation/eos-nation-roadmap-on-values-community-project-timeline-finances-and-transparency",
        "email":"info@eosnation.io",
        "branding":{
            "logo_256":"https://eosnation.keybase.pub/logo_256.png",
            "logo_1024":"https://eosnation.keybase.pub/logo_1024.png",
            "logo_svg":"https://eosnation.keybase.pub/logo.svg"
        },
        "location":{
            "name":"Toronto",
            "country":"CA",
            "latitude":43.655045,
            "longitude":-79.381306
        },
        "social":{
            "steemit":"eosnation",
            "twitter":"EOS_Nation",
            "facebook":"groups/EOSNation",
            "github":"EOS-Nation",
            "telegram":"EOSNation",
            "youtube":"channel/UCXgAY9DyooykrubRXw3xK1g",
            "reddit":"EOSNation",
            "keybase":"eosnation",
            "wechat":"Eosnation"
        }
    },
    "nodes":[
        {
            "location":{
                "name":"Toronto",
                "country":"CA",
                "latitude":43.655045,
                "longitude":-79.381306
            },
            "node_type":"full",
            "p2p_endpoint":"peer.eosn.io:9876",
            "bnet_endpoint":"peer.eosn.io:4321",
            "api_endpoint":"http://api.eosn.io",
            "ssl_endpoint":"https://api.eosn.io"
        },
        {
            "location":{
                "name":"Toronto",
                "country":"CA",
                "latitude":43.655045,
                "longitude":-79.381306
            },
            "node_type":"producer"
        }
    ]
    }
"""


@shared_task
def get_blockproducers():
    """
    {  
        "owner":"welovecaohai",
        "total_votes":"24073909594.59300231933593750",
        "producer_key":"EOS8ZiR9D92FiKtMjdrwCZWbq945YTxSionppGBS39Kynri859CTk",
        "is_active":1,
        "url":"http://www.zran.org",
        "unpaid_blocks":0,
        "last_claim_time":"1530361164000000",
        "location":0
    }
    """
    url = 'http://mainnet.eoscanada.com/v1/chain/get_producers'
    try:
        r = requests.post(url, data=json.dumps({'json': 'true', 'limit': 300}))
    except Exception as e:
        r = None
    if r:
        response = json.loads(r.text)
        data = response.get('rows')
        if data:
            bps = []
            for item in data:
                owner = item.get('owner')
                url = item.get('url')
                producer_key = item.get('producer_key')
            if owner and url and producer_key:
                bps.append(BlockProducer(account_name=owner,
                                         url=url, producer_key=producer_key))

        BlockProducer.objects.bulk_create(bps)


@shared_task
def update_bp_position():
    """
    {  
        "owner":"welovecaohai",
        "total_votes":"24073909594.59300231933593750",
        "producer_key":"EOS8ZiR9D92FiKtMjdrwCZWbq945YTxSionppGBS39Kynri859CTk",
        "is_active":1,
        "url":"http://www.zran.org",
        "unpaid_blocks":0,
        "last_claim_time":"1530361164000000",
        "location":0
    }
    """
    url = 'http://mainnet.eoscanada.com/v1/chain/get_producers'
    try:
        r = requests.post(url, data=json.dumps({'json': 'true', 'limit': 300}))
    except Exception as e:
        r = None
        print(str(e))
    if r:
        response = json.loads(r.text)
        # None if key is missing. We are covered here
        data = response.get('rows')
        if data:
            for item in data:
                owner = item.get('owner')
                url = item.get('url')
                producer_key = item.get('producer_key')
                total_votes = item.get('total_votes')
                try:
                    bp = BlockProducer.objects.get(
                        account_name=owner, producer_key=producer_key)
                    try:
                        bp_data = BlockProducerData.objects.create(block_producer=bp, unweighted_votes=total_votes, position=data.index(
                            item)+1)  # Our Index starts at 0. We can't have Position 0 though. +1
                        # Calculate Weighted Votes
                        # calculate_weighted(bp, total_votes) TODO
                    except Exception as e:
                        pass
                except Exception as e:
                    pass


@shared_task
def calculate_weighted(bp, unweighted_votes):
    """
        double stake2vote( int64_t staked ) {
            /// TODO subtract 2080 brings the large numbers closer to this decade
            double weight = int64_t( 
                (now() - (block_timestamp::block_timestamp_epoch / 1000)) / (seconds_per_day * 7) )  / double( 52 );
            return double(staked) * std::pow( 2, weight );
        }
    """
    # Calculate current epoch time
    now = timezone.now().timestamp()  # If youre using python 2 look for another way
    print(now)
    # More TODO


@shared_task
def fetch_bp_json():

    bps = BlockProducer.objects.all()
    filename = 'bp.json'
    for bp in bps:
        try:

            r = requests.get('{}/{}'.format(bp.url, filename), verify=False)
            print(bp.url)
            response = json.loads(r.text)
            details = response.get('org')
            if details:
                bp.display_name = details.get('candidate_name')
                bp.email = details.get('email')
                logos = details.get('branding')
                if logos:
                    # See function definition below
                    print('Found Logs')
                    is_downloadable(bp, logos.get('logo_256'))
                location = details.get('location')
                if location:
                    bp.country = location.get('country')
                    bp.latitude = location.get('latitude')
                    bp.longitude = location.get('longitude')
                    point = "POINT(%s %s)" % (location.get(
                        'latitude'), location.get('longitude'))
                    bp.geom = geos.fromstr(point)
                bp.save()
                print(bp.geom)
        except Exception:
           pass


@shared_task
def is_downloadable(bp, url):
    """
    Does the url contain a downloadable resource?
    """
    h = requests.head(url, allow_redirects=True, verify=False)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        downloadable = False
    if 'html' in content_type.lower():
        downloadable = False
    downloadable = True
    if downloadable:
        download_to_file_field(url, bp)
        # r = requests.get(url, allow_redirects=True)
        # get_filename_from_cd(bp, r.headers.get('content-disposition'), url, r)


@shared_task
def download_to_file_field(url, bp):
    with TemporaryFile() as tf:
        r = requests.get(url, stream=True, verify=False)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)
        tf.seek(0)
        bp.logo.save(basename(urlsplit(url).path), File(tf))

# @shared_task
# def get_filename_from_cd(bp, cd, url, r):
#     """
#     Get filename from content-disposition
#     """
#     if not cd:
#         get_filename_from_url(bp, url)
#     fname = re.findall('filename=(.+)', cd)
#     if len(fname) == 0:
#         get_filename_from_url(bp, url)
#     #
#     return fname[0]

# @shared_task
# def get_filename_from_url(bp, url):
#     try:
#         if url.find('/'):
#             filename = url.rsplit('/', 1)[1]
#     except Exception:
#         filename = None
#     if filename:
#         # Save
#         pass


# def save_image_to_model(bp, filename):
#     pass


# content_length = header.get('content-length', None)
# if content_length and content_length > 2e8:  # 200 mb approx
#   return False
