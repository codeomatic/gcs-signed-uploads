#!/usr/bin/env python
# Example using signed upload API

import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

UPLOAD_API_URL = os.getenv('UPLOAD_API_URL')


def get_upload_url_for(filename):
    resp = requests.post(UPLOAD_API_URL, json={'filename': filename},)
    if resp.status_code >= 400:
        print(resp.json())
        resp.raise_for_status()
    context = resp.json()
    return context['result']


def upload(paths):
    for path in paths:
        name = os.path.basename(path)
        upload_url = get_upload_url_for(name)
        print('Starting "{}" upload.'.format(name))
        with open(path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f)
        if upload_response.status_code >= 400:
            print(upload_response.json())
            upload_response.raise_for_status()
        print('done')


if __name__ == '__main__':
    upload(sys.argv[1:])
