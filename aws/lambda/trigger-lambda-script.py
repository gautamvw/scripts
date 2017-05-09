from __future__ import print_function
import boto3, json

def lambda_handler(event, context):
    client = boto3.client('lambda')
    resp = client.invoke(
        FunctionName='function_name',
        InvocationType='RequestResponse',
        ###Add params for child function here
        Payload = '{"account_ID":"","bucket":"","sns_topic":""}'
    )
    #print(resp)
    url_title = resp['Payload'].read()
    return url_title