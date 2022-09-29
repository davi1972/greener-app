import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

URL = 'https://41e6f7c3-a3ca-4f38-8422-d544beb68cfa-bluemix.cloudantnosqldb.appdomain.cloud'
API_KEY = 'cn0Qkx5QgWifCEXuzT24NF-NKy7WRjpn-QmbpHhQFG6o'
DB = 'greener'

def main(dict):
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)
    
    try:
        payload = dict['payload']
        
        attributes = payload['attributes']
        details = payload['details']
        host = payload['host']
        img_path = 'n/a'

        if 'link' in payload:
            link = payload['link']
        else:
            link = 'n/a'
        
        location = payload['location']
        name = payload['name']
        num_people_responded = 'n/a'
        recommend_count = 0
        
        new_event = Document(
            attributes=attributes,
            details=details,
            host=host,
            imgPath=img_path,
            link=link,
            location=location,
            name=name,
            numPeopleResponded=num_people_responded,
            recommendCount=recommend_count
        )
        
        response = service.post_document(
            db=DB,
            document=new_event
        ).get_result()
        
        if 'error' in response:
            print(f'{name} was not written successfully as no successful id was returned for it upon writing to the {DB} database.')
        
        return { 'payload': response }

    except KeyError as e:
        print(e)
        return { 'error': 'KeyError, refer to logs' }
        
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Event creation failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Event creation failed, message - {ae.message}' }