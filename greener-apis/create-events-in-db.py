import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1, Document, BulkDocs
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

URL = 'https://41e6f7c3-a3ca-4f38-8422-d544beb68cfa-bluemix.cloudantnosqldb.appdomain.cloud'
API_KEY = 'cn0Qkx5QgWifCEXuzT24NF-NKy7WRjpn-QmbpHhQFG6o'
DB = 'greener'

def create_bulk_docs(service, item_list):
    doc_ids = []
    new_events = []
    for item in item_list:
        attributes = item['attributes']
        details = item['details']
        host = item['host']
        img_path = item['imgPath']
        link = item['link']
        location = item['location']
        name = item['name']
        num_people_responded = item['numPeopleResponded']
        recommend_count = 0
        
        penultimate_slash = link.find('events/') + 7
        final_slash = link[penultimate_slash:].find('/') + penultimate_slash
        doc_id = link[penultimate_slash:final_slash]
        doc_ids.append(doc_id)
        
        new_event = Document(
            id=doc_id,
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
        new_events.append(new_event)
    
    return BulkDocs(docs=new_events), doc_ids

def main(dict):
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)
    
    try:
        payload = dict['payload']
        bulk_docs, doc_ids = create_bulk_docs(service, payload)
        
        responses = service.post_bulk_docs(
          db=DB,
          bulk_docs=bulk_docs
        ).get_result()
        all_returned_doc_ids = [event_response['id'] for event_response in responses if 'error' not in event_response]
        
        for event, doc_id in zip(payload, doc_ids):
            if doc_id in all_returned_doc_ids:
                event['id'] = doc_id
            else:
                print(f'{event["name"]} with id {doc_id} was not written successfully as no successful id was returned for it upon writing to the {DB} database.')
        
        return { 'payload': responses }
    
    except KeyError as e:
        print(e)
        return { 'error': 'KeyError, refer to logs' }
    
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Event(s) creation failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Event(s) creation failed, message - {ae.message}' }