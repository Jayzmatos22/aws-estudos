import json
import urllib.request

def lambda_handler(event, context):
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/5?formato=json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }