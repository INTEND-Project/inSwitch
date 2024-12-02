from typing import Literal
import json


WORKLOADS = {
    'ngix':{
        '1.27.2': 'bac63c699823'
    },
    'nodejs':{
        '23.2.0': '5da72944732c'
    },
    'alarm_record':{
        '1.1': 'cf14424f4cbb',
        '1.2': '708d07cbbd21',
        '1.3': '2d399dd9eb06'
    },
    'mqtt_sender':{
        '1.21.1': 'fcb024769e03'
    },
    'energy_aggregator':{
        '1.1': '7341f42396d6'
    },
    'energy_collector':{
        '1.1.1': '5027985c4858'
    }
}


# This is a mockup of the real python client for Nerve API
# It has the same method signature, but only print out the payload/data
# Original code here: https://github.com/tttech-nerve/nerve-api-examples/blob/master/nerveapi/session.py
# We did not include login, etc., at the moment
def make_request(endpoint:str, method:Literal['GET', 'POST', 'PUT']='GET', data:str=None, files=None, workaround=None) -> str:
    if endpoint.startswith("/nerve/dna/") and method == 'PUT':
        print(f"PUT: {endpoint}:\n{data}")
        return "done"
    if endpoint == "/nerve/v3/workloads" and method == 'GET':
        return ', '.join(WORKLOADS.keys())

    if endpoint.startswith("/nerve/v3/workloads/") and not ("/versions" in endpoint) and method == 'GET':
        workload = endpoint.split('/')[-1]
        print(workload)
        return ', '.join(WORKLOADS.get(workload).keys())
    
    if endpoint.startswith("/nerve/v3/workloads/") and '/versions/' in endpoint:
        workload = endpoint.split('/')[4]
        version = endpoint.split('/')[6]
        result = {
            "name": workload,
            "version": version,
            "hash": WORKLOADS[workload][version]
        }
        return json.dumps(result)

if __name__=="__main__":
    print(make_request("/nerve/v3/workloads"))
    print(make_request("/nerve/v3/workloads/alarm_record"))
    print(make_request("/nerve/v3/workloads/alarm_record/versions/1.2"))