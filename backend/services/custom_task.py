# CUSTOM CHAT
# This module contains customizable code for orchestrating multi-agent interactions.
# 
# IMPORTANT: This file must always contain the `custom_chat` function.
# This function takes a user intent as input, coordinates multiple agents,
# and returns the complete chat history as a single string for analysis.
#
# You are free to modify the agent configurations and logic,
# as long as `custom_chat` remains present and functional.

from inswitch.agent.basic import get_chat_agent, get_fixed_reply_agent
from inswitch.agent.apiagent import ApiAgent

from usecases.fill.filluc.mockupnerv.session import make_request

with open("./data/mockup_single_machine_tripple.txt", "r") as api_doc:
    content = api_doc.read()

knowledge_provider = get_fixed_reply_agent(
    'knowledge_provider',
    reply=content
)

decision_maker_message = '''You are the decision maker.
You get the user's intents, together with some knowledge about 
what machines, services, workloads, version etc., are avaliable in the system.
Based on these, you decide which workloads, and their versions. should be deployed on which machine.
Remember to always and only use the concrete version numbers, not the version names.
Reply with the deployment plan, i.e., machine serial number, workload names, and their version numbers. With label and values'''

decision_maker = get_chat_agent(
    "decision_maker",
    system_message=decision_maker_message
)

with open("./data/nerve_api_dna.txt", "r") as api_doc:
    content = api_doc.read()

api_doc_provider = get_fixed_reply_agent(
    'api_doc_provider', 
    reply=content
)

moderator = get_fixed_reply_agent(
    name="moderator",
    reply = ""
)

nerv_api_system_message = '''
You have access to a tool to call the Nerve DNA API to fulfil the user's intent.
The task is in the context.
You will get from the context a document of the Nerve DNA API.
Using the document, you will figure out how to call the API, i.e., using what endpoint and method.
You will also need to generate the configuration file as the data of the api call, to fulfil the task assigned to you.
If you don't have the version for some workloads, 
you need to call the API to get the available version numbers and their hash code. Use the first version by default 
If you don't have the hash code, call the API using the workload and version to get its unique information, which include hash code.
'''

nerve_api_agent = ApiAgent(
    "nerve_api_agent", 
    system_message=nerv_api_system_message, 
    max_internal_turns=3
)


nerve_api_agent.register_api_function(
    make_request,
    description = "This is the function to send a request to the Nerve API for deploying workloads etc. "
)

def custom_chat(user_intent):
    """
    Runs a multi-agent conversation based on the user's intent and returns the full chat as a string.

    Parameters
    ----------
    user_intent : str
        The content of the user intent.

    Returns
    -------
    str
        A string representation of the chat results, containing the full conversation
        between the agents.
    """

    intent_provider = get_fixed_reply_agent(
        'intent_provider',
        reply = user_intent
    )

    decision_chat_results = moderator.initiate_chats(
        [
            {
                "recipient": intent_provider,
                "message": "what do you want?",
                "max_turns": 1,
                "summary_method": "last_msg"
            },
            {
                "recipient": knowledge_provider,
                "message": "What do you know about the system",
                "max_turns": 1,
                "summary_method": "last_msg"
            },
            {
                "recipient": decision_maker,
                "message": "What should be deployed",
                "max_turns": 1,
                "summary_method": "last_msg"
            }
        ]
    )

    deploy_plan = decision_chat_results[-1].summary

    deployment_plan_announcer = get_fixed_reply_agent(
        'deployment_plan_announcer',
        reply=deploy_plan
    )

    chat_result = moderator.initiate_chats(
        [
            {
                "recipient": deployment_plan_announcer,
                "message": "What should be deployed? on which machine?",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": api_doc_provider,
                "message": "Please provide me the api doc",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": nerve_api_agent,
                "message": "you can see the intent and the knowledge in the context",
                "max_turns": 1,
                "summary_method": "last_msg"
            }
        ]
    )

    return repr(decision_chat_results+chat_result)