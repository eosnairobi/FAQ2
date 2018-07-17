import requests
import json

from .models import Tool

def get_status():
    tools = Tool.objects.all()
    for tool in tools:

        try:
            url = tool.url
            response = requests.get(url, verify=False) # We sometimes have issues with SSL Certs. Ignoring just a litle won't do us no much harm
            if response == '200':
                tool.is_live = True
            else:
                tool.is_live = False
            tool.save()
        except Exception:
            pass