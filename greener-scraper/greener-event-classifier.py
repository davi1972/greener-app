import sys
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ClassificationsOptions
from ibm_cloud_sdk_core import ApiException

# NLU credentials
API_KEY = 'Xk8QenO4AEzbij8TtybNsJvoqyaNH238xYvGwgcDKY_w'
URL = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/bdb35005-85ff-4193-bbca-854c68a26777'

# Constants for classification
CLASSIFIER_MODEL_ID = '6c9d997a-c9dc-402a-bb36-3bfd9fd26031'
ATTRIBUTE_LIST = ["community", "environment", "food", "physical", "virtual"]
CONFIDENCE_THRESHOLD = 0.3

def connect_NLU_service():
    auth = IAMAuthenticator(API_KEY)
    nlu = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=auth)
    nlu.set_service_url(URL)
    print('Successfully connected with the NLU service')
    return nlu

def main(dict):
    try:
        nlu = connect_NLU_service()
        
        event_pool = dict['payload']
        classified_event_pool = []
        for event in event_pool:
            response = nlu.analyze(text=event['details'], features=Features(classifications=ClassificationsOptions(model=CLASSIFIER_MODEL_ID))).get_result()
            print(f"Details of this instance of usage of classification model:\n{response['usage']}")
            
            resp_attr_list = response['classifications']
            attr_dict = {}
            for resp_attr_level in resp_attr_list:
                if resp_attr_level['confidence'] >= CONFIDENCE_THRESHOLD:
                    attr_dict[resp_attr_level['class_name']] = 1
                else:
                    attr_dict[resp_attr_level['class_name']] = 0
            
            for attribute in ATTRIBUTE_LIST:
                if attribute not in attr_dict.keys():
                    attr_dict[attribute] = 0
            
            if 1 not in attr_dict.values():
                attr_dict = {"community": 0, "environment": 1, "food": 0, "physical": 0, "virtual": 0}
            
            event['attributes'] = attr_dict
            classified_event_pool.append(event)
        
        return { 'payload': classified_event_pool }

    except KeyError as e:
        print(e)
        return { 'error': 'KeyError, refer to logs' }
    
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Event classification failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Event classification failed failed, message - {ae.message}' }