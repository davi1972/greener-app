import sys
import json
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

# NLU credentials
API_KEY = 'Xk8QenO4AEzbij8TtybNsJvoqyaNH238xYvGwgcDKY_w'
URL = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/bdb35005-85ff-4193-bbca-854c68a26777'

def connect_NLU_service():
    auth = IAMAuthenticator(API_KEY)
    nlu = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=auth)
    nlu.set_service_url(URL)
    print('Successfully connected with the NLU service')
    return nlu

def train_model(nlu):
    event_pool = get_events()
    
    data = []
    for event in list(event_pool.values()):
        event_attributes = event['attributes']
        to_remove = ''
        labels = [event_attr[0] if event_attr[1] == 1 else to_remove for event_attr in list(event_attributes.items())]
        while to_remove in labels:
          labels.remove(to_remove)
        event_training_data = {
            'text': event['details'],
            'labels': labels,
        }
        data.append(event_training_data)
    
    training_data_filename = 'training_data.json'
    
    with open(training_data_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    with open(training_data_filename, 'rb') as file:
        model = nlu.create_classifications_model(language='en', training_data=file, training_data_content_type='application/json', name='GreenerEventClassificationModel', model_version='1.0.0').get_result()
        print("Created an NLU Classifications model, details returned.")
        return json.dumps(model, indent=4)
    
def get_model_info(nlu, model_id):
    model_to_view = nlu.get_classifications_model(model_id=model_id).get_result()
    print("Information about the specified NLU Classifications model returned.")
    return json.dumps(model_to_view, indent=4)

def delete_model(nlu, model_id):
    deleted_model = nlu.delete_classifications_model(model_id=model_id)
    updated_models_list = nlu.list_classifications_models().get_result()
    print("Deleted NLU Classifications model, details of remaining models returned.")
    return json.dumps(updated_models_list, indent=4)

def get_model_list(nlu):
    updated_models_list = nlu.list_classifications_models().get_result()
    return json.dumps(updated_models_list, indent=4)

def get_events():
    response = requests.get("https://fcd54591.us-south.apigw.appdomain.cloud/list")
    base_param = response.json()
    
    event_pool = {}
    
    for item in base_param["rows"]:
        document = item["doc"]
        if "username" not in document:
            event_pool[document["_id"]] = document
    
    return event_pool

def main(dict):
    try:
        nlu = connect_NLU_service()
        
        model_json = train_model(nlu)
        
        # model_json = get_model_list(nlu)
        
        # model_id = ''
        # model_json = get_model_info(nlu, model_id)
        
        # model_id_for_deletion = ''
        # model_json = delete_model(nlu, model_id_for_deletion)
        
        model_dict = json.loads(model_json)
        
        return { 'payload' : model_dict }

    except KeyError as e:
        print(e)
        return { 'error': 'KeyError, refer to logs' }
    
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'NLU Classifier training failed failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'NLU Classifier training failed, message - {ae.message}' }