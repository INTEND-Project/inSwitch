from typing import Literal
import json
import sys

# Add path
sys.path.append('../../../..')


from inswitch.llm.model import get_openai_model_config
from pydantic import BaseModel, model_validator, ValidationError
from openai import OpenAI

llm_config = get_openai_model_config()

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

def filter_task(message: str) -> str:

    class NerveTaskType(BaseModel):
        list_workloads: bool 
        create_workload: bool 
        create_label: bool
        get_labels: bool
        delete_label: bool
        create_wl_template: bool
        delete_workloads: bool 
        list_nodes: bool 
        reboot_nodes: bool 
        start: bool 
        stop: bool 
        restart: bool

    class NerveOperationType(BaseModel):
        GET: bool
        POST: bool
        PUT: bool
        DELETE: bool
        MATCH: bool

    class CombinedResponseFormat(BaseModel):
        task: NerveTaskType
        operation: NerveOperationType

    client = OpenAI(api_key=llm_config['api_key'])
    
    completion_with_compliance_check = client.beta.chat.completions.parse(
        model=llm_config["model"],
        messages=[
            {"role": "system", "content": "Determine what kind of Nerve API task your input is, and what kind of HTTP method/operation is expected."},
            {
                "role": "user",
                "content": message
            }
        ],
        response_format=CombinedResponseFormat,
    )
    parsed_responses = completion_with_compliance_check.choices[0].message.parsed
    tasks = parsed_responses.task
    operations = parsed_responses.operation
    true_tasks = []
    true_operations = []
    for task in tasks:
        if task[1]:
            true_tasks.append(task[0])
    for operation in operations:
        if operation[1]:
            true_operations.append(operation[0]) 
    return str("Type of Nerve API task: "+ str(true_tasks) + " -- "+ "The expected HTTP method: " + str(true_operations))


if __name__=="__main__":
    print(make_request("/nerve/v3/workloads"))
    print(make_request("/nerve/v3/workloads/alarm_record"))
    print(make_request("/nerve/v3/workloads/alarm_record/versions/1.2"))

    print(filter_task("Deploy the following workloads for Machine: M00001 (Type: MTC) - Workload: ngix, Version: ngix_27 (1.27.2) - Workload: nodejs, Version: nodejs_23 (23.2.0) - Workload: alarm_record - Workload: mqtt_sender"))
    print(filter_task("Start the workload with name ngix"))
    print(filter_task("Get all of the labels"))




