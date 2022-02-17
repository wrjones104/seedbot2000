import requests
import json
import os


def generate_v1_seed(flags, seed_desc):
    url = "https://ff6wc.com/api/generate"
    if seed_desc:
        payload = json.dumps({
            "key": os.getenv("ff6wc_api_key"),
            "flags": flags,
            "description": seed_desc
        })
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        payload = json.dumps({
            "key": os.getenv("ff6wc_api_key"),
            "flags": flags
        })
        headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    if 'url' not in data:
        return KeyError(f'API returned {data} for the following flagstring:\n```{flags}```')
    return data
