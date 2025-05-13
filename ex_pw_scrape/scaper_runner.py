from dotenv import load_dotenv
import os
import requests

load_dotenv()

ex_ip = os.environ.get('EXTERNAL_IP')

def scrape(url):
    response = requests.get(f'http://{ex_ip}/scrape', params= {'url' : url})
    if response.status_code == 200 :
        data = response.json()
        print(f'Result : {data}')
    else :
        print('Error:', response.status_code, response.text)
