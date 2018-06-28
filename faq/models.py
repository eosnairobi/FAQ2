from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
"""
{
    "tags":[
      "transactions",
      "action"
],
"owner":{
  "reputation":31,
  "user_id":1715,
  "user_type":"registered",
  "profile_image":"https://www.gravatar.com/avatar/ec081860101262a9161af88172b9fce5?s=128&d=identicon&r=PG&f=1",
  "display_name":"mochunhei",
  "link":"https://eosio.stackexchange.com/users/1715/mochunhei"
},
"is_answered":false,
"view_count":29,
"answer_count":1,
"score":1,
"last_activity_date":1530051695,
"creation_date":1529925884,
"question_id":1147,
"link":"https://eosio.stackexchange.com/questions/1147/how-to-perform-something-when-my-contract-receives-a-eosio-token-transfer-notifi",
"title":"How to perform something when my contract receives a eosio.token transfer notification?"
}
"""


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = models.TextField(max_length=10000)
    se_link = models.URLField(null=True)
    is_answered = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    se_question_id = models.PositiveIntegerField(null=True)
    score = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='tags')

    # def __str__(self):
    # return self.


class Answer(models.Model):
    """
    {
    "owner":{
      "reputation":1,
      "user_id":1426,
      "user_type":"registered",
      "profile_image":"https://www.gravatar.com/avatar/592a37499b5c36fd71c2fdbe6a0e1dc5?s=128&d=identicon&r=PG&f=1",
      "display_name":"bread1984",
      "link":"https://eosio.stackexchange.com/users/1426/bread1984"
    },
       "is_accepted":false,
       "score":0,
       "last_activity_date":1530051695,
       "creation_date":1530051695,
       "answer_id":1173,
       "question_id":1147
    }
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    body = models.TextField(max_length=10000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    se_question_id = models.IntegerField()
    is_accepted = models.BooleanField(default=False)
    se_answer_id = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
