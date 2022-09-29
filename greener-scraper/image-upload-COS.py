import ibm_boto3
from ibm_botocore.client import Config, ClientError
from ibm_cloud_sdk_core import ApiException
import requests

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.private.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "7Fnm3zAgMRGIIYKAZ0EjlT25QqRWbDNdfj1PerzBY7jP"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/4a172a5907e94547acdc4c2e9e49b69e:f93f14e0-79af-4081-a7b5-79cec2d54293::"

BUCKET_NAME = "greener-event-pictures"

def upload_large_file(bucket_name, item_name, file_path):
    print("Starting large file upload for {0} to bucket: {1}".format(item_name, bucket_name))

    # set the chunk size to 5 MB
    part_size = 1024 * 1024 * 5

    # set threadhold to 5 MB
    file_threshold = 1024 * 1024 * 5

    # Create client connection
    cos_cli = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )

    # set the transfer threshold and chunk size in config settings
    transfer_config = ibm_boto3.s3.transfer.TransferConfig(
        multipart_threshold=file_threshold,
        multipart_chunksize=part_size
    )

    # create transfer manager
    transfer_mgr = ibm_boto3.s3.transfer.TransferManager(cos_cli, config=transfer_config)

    try:
        # initiate file upload
        future = transfer_mgr.upload(file_path, bucket_name, item_name)

        # wait for upload to complete
        future.result()

        print("Large file upload complete!")
    except Exception as e:
        print("Unable to complete large file upload: {0}".format(e))
    finally:
        transfer_mgr.shutdown()

def grab_image(image_url, filename):
    url = str(image_url)
    r = requests.get(url, allow_redirects=True)
    print('img_path is: {}'.format(url))
    with open(filename, 'wb') as file:
        file.write(r.content)
    return filename

def main(dict):
    try:
        payload = dict['payload']
        
        for item in payload:
            link = item['link']
            penultimate_slash = link.find('events/') + 7
            final_slash = link[penultimate_slash:].find('/') + penultimate_slash
            
            doc_id = link[penultimate_slash:final_slash]
            filename = doc_id + ".jpg"
            file_path = "./" + filename
            img_path = item['imgPath']
            
            filename = grab_image(img_path, filename)
            upload_large_file(BUCKET_NAME, filename, file_path)
        
        return dict
    
    except KeyError as e:
        print(e)
        return { 'error': 'KeyError, refer to logs' }
    
    except ApiException as ae:
        if ('reason' in ae.http_response.json()):
            return { 'message': f'Image upload to COS failed, reason - {ae.http_response.json()["reason"]}' }
        else:
            return { 'message': f'Image upload to COS failed, message - {ae.message}' }