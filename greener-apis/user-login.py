import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

URL = 'https://41e6f7c3-a3ca-4f38-8422-d544beb68cfa-bluemix.cloudantnosqldb.appdomain.cloud'
API_KEY = 'cn0Qkx5QgWifCEXuzT24NF-NKy7WRjpn-QmbpHhQFG6o'
DB = 'greener-users'

def main(dict):
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)
    
    try:
        username = dict['username']
        password = dict['password']
        
        response = service.get_document(
          db=DB,
          doc_id=username
        ).get_result()
        
        if response['password'] == password:
            return { 'message': "Login successful" }
        else:
            return { 'message': "Login failed, password incorrect" }
        
    except KeyError as e:
        print(e)
        return { 'message': 'Login failed, username or password not provided' }
        
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Login failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Login failed, message - {ae.message}' }