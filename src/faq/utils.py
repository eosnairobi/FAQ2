from accounts.models import User
from .models import Question, Answer, Tag

import requests
import json


def get_questions():
    """
        Fetch Questions from eosio.stackexchange
    """
    count = 1
    for i in range(6):
        r = requests.get('https://api.stackexchange.com/2.2/questions?filter=withbody&site=eosio&pagesize=100&page={}'.format(count))
        data = json.loads(r.text)
        for item in data['items']:
            own = item['owner']['user_id']
            dsp = item['owner']['display_name']
            try:
                owner = User.objects.get(username=own, se_display_name=dsp)
            except Exception:
                owner = None
            tags = item['tags']
            ts = []
            if owner:
                for tag in tags:
                    t, created = Tag.objects.get_or_create(name=tag)
                    ts.append(t)
                q = Question.objects.create(owner=owner, se_question_id=item['question_id'], title=item['title'], body=item[
                                            'body'], se_link=item['link'], is_answered=item['is_answered'], score=item['score'])
                for t in ts:
                    q.tags.add(t)
                q.save()
        count += 1
        print(count)


def get_answers():
    """
        Fetch Answers from Stackexchange
    """
    count = 1
    for i in range(200):  # TODO : Fetch number of all items first
        r = requests.get('http://api.stackexchange.com/2.2/answers?site=eosio&filter=!b1MMEb*6iF.PM5&pagesize=100&page={}'.format(count))
        data = json.loads(r.text)
        for item in data['items']:
            own = item['owner']['user_id']
            dsp = item['owner']['display_name']
            qn_id = item['question_id']
            try:
                owner = User.objects.get(username=own, se_display_name=dsp)
                question = Question.objects.get(se_question_id=qn_id)
            except Exception:
                owner = None
                question = None
            if owner and question:
                Answer.objects.create(owner=owner, question=question, body=item['body'],
                                      se_question_id=qn_id, is_accepted=item['is_accepted'],
                                      se_answer_id=item['answer_id'], score=item['score'])

        count += 1
        print(count)
