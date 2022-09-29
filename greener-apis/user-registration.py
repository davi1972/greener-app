import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

URL = 'https://41e6f7c3-a3ca-4f38-8422-d544beb68cfa-bluemix.cloudantnosqldb.appdomain.cloud'
API_KEY = 'cn0Qkx5QgWifCEXuzT24NF-NKy7WRjpn-QmbpHhQFG6o'
DB = 'greener-users'

TYPE = 'User'
DEFAULT_ATTRIBUTES = {
    "community": 0.5,
    "environment": 0.5,
    "food": 0.5,
    "physical": 0.5,
    "virtual": 0.5
}
ATTENDED_EVENTS = {}
LIKED_EVENTS = {}
EVENT_SCORES = {}

def main(dict):
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)
    
    try:
        username_reg = dict['username']
        password_reg = dict['password']
        
        new_user = Document(
            id=username_reg,
            password=password_reg,
            type=TYPE,
            attributes=DEFAULT_ATTRIBUTES,
            attendedEvents=ATTENDED_EVENTS,
            likedEvents=LIKED_EVENTS,
            eventScores=EVENT_SCORES
        )
        
        response = service.post_document(db=DB, document=new_user).get_result()

        return { 'message': { 'success': response } }
        
    except KeyError as e:
        print(e)
        return { 'message': 'Registration failed, username or password not provided' }
        
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Registration failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Registration failed, message - {ae.message}' }