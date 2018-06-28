from .models import User
import json
import requests


def get_users():
    count = 1
    for i in range(19):
        r = requests.get('https://api.stackexchange.com/2.2/users?site=eosio&pagesize=100&page={}'.format(count))
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
