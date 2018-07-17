import copy  # Copies instances of Image
import cStringIO  # Used to imitate reading from byte file
import imghdr  # Used to validate images
import json
import urllib2  # Used to download images
import urlparse  # Cleans up image urls

import requests
from PIL import Image  # Holds downloaded image and verifies it

from django.contrib.gis import geos
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

from .models import BlockProducer, BlockProducerData, User


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
                print(count)
            else:
                print(count)


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
        print(str(e))

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


def fetch_bp_json():

    bps = BlockProducer.objects.all()
    filename = 'bp.json'
    for bp in bps:
        try:

            r = requests.get('{}/{}'.format(bp.url, filename))
            print(bp.url)
            response = json.loads(r.text)
            details = response.get('org')
            if details:
                bp.display_name = details.get('candidate_name')
                bp.email = details.get('email')
                logos = details.get('branding')
                if logos:
                    logo = save_image_from_url(bp, logos.get('logo_256'))  # See function definition below
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
        except Exception as e:
            print(str(e))




def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    # img_temp.flush()

    model.logo.save("image.jpg", File(img_temp), save=True)


# def download_image(url):
#     """Downloads an image and makes sure it's verified.

#     Returns a PIL Image if the image is valid, otherwise raises an exception.
#     """
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}  # More likely to get a response if server thinks you're a browser
#     r = urllib2.Request(url, headers=headers)
#     request = urllib2.urlopen(r, timeout=10)
#     # StringIO imitates a file, needed for verification step
#     image_data = cStringIO.StringIO(request.read())
#     # Creates an instance of PIL Image class - PIL does the verification of file
#     img = Image.open(image_data)
#     # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
#     img_copy = copy.copy(img)
#     if valid_img(img_copy):
#         return img
#     else:
#         # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
#         raise Exception(
#             'An invalid image was detected when attempting to save a BP!')


# def valid_img(img):
#     """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
#     type = img.format
#     if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
#         try:
#             img.verify()
#             return True
#         except:
#             return False
#     else:
#         return False


# # def save(self, url='', *args, **kwargs):
# #     if self.prod_img != '' and url != '':  # Don't do anything if we don't get passed anything!
# #         image = download_image(url)  # See function definition below
# #         try:
# #             filename = urlparse.urlparse(url).path.split('/')[-1]
# #             self.prod_img = filename
# #             tempfile = image
# #             # Will make a file-like object in memory that you can then save
# #             tempfile_io = cStringIO.StringIO()
# #             tempfile.save(tempfile_io, format=image.format)
# #             # Set save=False otherwise you will have a looping save method
# #             self.prod_img.save(filename, ContentFile(
# #                 tempfile_io.getvalue()), save=False)
# #         except Exception as e:
# #             print("Error trying to save model: saving image failed: " + str(e))
# #             pass
# #     super(Product, self).save(*args, **kwargs)  # We've gotten the image into the ImageField above...now we actually need to save it. We've redefined the save method for Product, so super *should* get the parent of class Product, models.Model and then run IT'S save method, which will save the Product like normal
