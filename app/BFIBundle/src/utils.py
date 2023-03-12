import requests
import json
import csv
from models import Interaction,Taxonomy

def get_version(api_url) -> str:
    '''
    Get databse version 
    '''
    version_url = api_url + '/interactions/db/version'
    version_request = requests.get(version_url)
    
    return version_request.json()

def data_dump(api_url,tsv: bool=True) -> None:
    """Data dump of bacterial fungal interactions

    Args:
        tsv (bool, optional): If false, will dump data into a json file.
    """
    dump_url = api_url + '/interactions/'
    data_dump_json = requests.get(dump_url).json()
    for record in data_dump_json:
        record.pop('_id')
    if tsv:
        with open(f'bfi-source-{get_version(api_url)}.tsv','w') as tsv_dump:
            dict_writer = csv.DictWriter(tsv_dump, sorted(list(Interaction.__fields__.keys())), delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(data_dump_json)
    else:
        with open(f'bfi-source-{get_version(api_url)}.json','w') as json_dump:
            json.dump(data_dump_json,json_dump,ensure_ascii=False, indent=4,sort_keys=True)