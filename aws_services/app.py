import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

url = 'https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
regions_map = {
    'Northern Virginia': 'us-east-1',
    'Ohio': 'us-east-2',
    'Oregon': 'us-west-2',
    'Northern California': 'us-west-1',
    'Montreal': 'ca-central-1',
    'São Paulo': 'sa-east-1',
    'AWS GovCloud (US-West)': 'us-gov-west-1',
    'AWS GovCloud (US-East)': 'us-gov-east-1',
    'Ireland': 'eu-west-1',
    'Frankfurt': 'eu-central-1',
    'London': 'eu-west-2',
    'Paris': 'eu-west-3',
    'Stockholm': 'eu-north-1',
    'Bahrain': 'me-south-1',
    'Singapore': 'ap-southeast-1',
    'Tokyo': 'ap-northeast-1',
    'Osaka': 'ap-northeast-3',
    'Sydney': 'ap-southeast-2',
    'Seoul': 'ap-northeast-2',
    'Mumbai': 'ap-south-1',
    'Hong Kong': 'ap-east-1',
    'Beijing': 'cn-north-1',
    'Ningxia': 'cn-northwest-1',
    'Cape Town': 'af-south-1',
    'Milan': 'eu-south-1'
}


def lambda_handler(event, context):
    region_codes = True
    if event['queryStringParameters'] is not None:
        if 'region_names' in event['queryStringParameters']:
            if event['queryStringParameters']['region_names'] == 'true':
                region_codes = False

    last_updated_at = get_last_updated_at()

    records = []
    for i in range(3):
        table = soup.find_all('table')[i]
        df = pd.read_html(str(table))
        data = json.loads(df[0].to_json(orient='records'))

        for record in data:
            records.append(record)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {'last_updated': last_updated_at,
             'data': transform(records, region_codes)
             })
    }


def get_last_updated_at():
    last_updated_text = soup.find("div", {"class": "lb-rtxt"}).getText().split(':')[1]
    last_updated = datetime.strptime(last_updated_text, ' %B %d, %Y. ')

    return last_updated.strftime('%Y-%m-%d')


def transform(records, region_codes=False):
    output = {}
    for record in records:
        service = ''
        available_regions = []
        for key in record:
            if key == 'Services Offered:':
                service = record[key]
            else:
                if record[key] == '✓':
                    region_name = key.replace("*", '')
                    if region_codes is True:
                        region_name = regions_map[region_name]
                    available_regions.append(region_name)

        service = " ".join(re.findall("[a-zA-Z()-]+", service))
        if service in output:
            output[service].extend(available_regions)
        else:
            output[service] = available_regions
        output[service].sort()

    return output
