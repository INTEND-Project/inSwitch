# SERVICE
# Contains logic

from repositories import intent_repository as repository
from services import core_agents
from services.custom_task import custom_chat
from services.core_agents import result_extractor, summary_extractor, moderator

import datetime as dt
import time
import uuid

def get_all_intents():
    """
    Function used to analyse the response of the database to get all the intents stored and
    to format them.
    
    Returns
    -------
    intents : List
        List of intents.
    """

    response = repository.fetch_intents_from_graphdb()

    if response.status_code != 200:
        return None
    
    intents_db = response.json()["results"]["bindings"]

    if not intents_db:
        return None

    intents = []

    for i in intents_db:
        id = i['id']["value"].split("/")[-1]

        intent = {
            "id": id,
            "author": i["authorName"]["value"],
            "content": i["content"]["value"],
            "creationDate": i["creationDate"]["value"],
            "lastUpdateDate": i["lastUpdate"]["value"]
        }
        intents.append(intent)
    
    return intents

def get_all_intents_json_ld():
    """
    Function used to format the list of intent in JSON-LD format.
    
    Returns
    -------
    jsonld_data : List
        List of intents in JSON-LD format.
    """
    
    intents = get_all_intents()
    
    if not intents:
        return None
    
    # Definition of the context
    jsonld_data = {
        "@context": {
            "ex": "http://example.com/intent/",
            "icm": "http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
    }
    jsonld_data["intents"] = []

    for intent in intents:
        id = intent['id'].split("/")[-1]
        
        creation_date_obj = dt.datetime.fromisoformat(intent['creationDate'])
        update_date_obj = dt.datetime.fromisoformat(intent['lastUpdateDate'])

        intent_data = {
            "@id": f"ex:{id}",
            "@type": "icm:Intent",
            "ex:author": {
                "@id": f"ex:person/{intent['author'].replace(' ', '_')}",
                "@type": "foaf:Person",
                "foaf:name": intent['author']
            },
            "ex:content": intent['content'],
            "dcterms:created": {
                "@value": creation_date_obj.isoformat(),
                "@type": "xsd:dateTime"
            },
            "dcterms:modified": {
                "@value": update_date_obj.isoformat(),
                "@type": "xsd:dateTime"
            }
        }
        jsonld_data["intents"].append(intent_data)

    return jsonld_data

def select_intent_from_id(intent_id : str):
    """
    Function used to analyse the response of the database to get an intent from its ID and
    to format it.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    
    Returns
    -------
    intent : Dictionary
        The intent with all its attributes.
    """
    
    response = repository.select_intent_from_graphdb(intent_id)

    if response.status_code != 200:
        return None

    intent_db = response.json()["results"]["bindings"][0]

    if not intent_db:
        return None

    id = intent_db['id']["value"].split("/")[-1]

    intent = {
        "id": id,
        "author": intent_db["authorName"]["value"],
        "content": intent_db["content"]["value"],
        "creationDate": intent_db["creationDate"]["value"],
        "lastUpdateDate": intent_db["lastUpdate"]["value"]
    }
    
    return intent

def select_intent_json_ld_from_id(intent_id : str):
    """
    Function used to format an intent in JSON-LD format.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    
    Returns
    -------
    jsonld_data : Dictionary
        The intent with all its attributes in JSON-LD format.
    """
    
    response = repository.select_intent_from_graphdb(intent_id)

    if response.status_code != 200:
        return None

    intent_db = response.json()["results"]["bindings"][0]

    if not intent_db:
        return None

    id = intent_db['id']["value"].split("/")[-1]
    
    creation_date_obj = dt.datetime.fromisoformat(intent_db["creationDate"]["value"])
    update_date_obj = dt.datetime.fromisoformat(intent_db["lastUpdate"]["value"])

    jsonld_data = {
        # Definition of the context
        "@context": {
            "ex": "http://example.com/intent/",
            "icm": "http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        },
        "@id": f"ex:{id}",
        "@type": "icm:Intent",
        "ex:author": {
            "@id": f"ex:person/{intent_db["authorName"]["value"].replace(' ', '_')}",
            "@type": "foaf:Person",
            "foaf:name": intent_db["authorName"]["value"]
        },
        "ex:content": intent_db["content"]["value"],
        "dcterms:created": {
            "@value": creation_date_obj.isoformat(),
            "@type": "xsd:dateTime"
        },
        "dcterms:modified": {
            "@value": update_date_obj.isoformat(),
            "@type": "xsd:dateTime"
        }
    }
    
    return jsonld_data

def get_all_intent_reports_of_intent(intent_id : str):
    """
    Function used to analyse the response of the database to get all the intent reports 
    of an intent from its ID and to format them.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    
    Returns
    -------
    intent_reports : List
        The list of all of the intent reports and their attributes.
    """
    
    if not select_intent_from_id(intent_id):
        return None
    
    response = repository.fetch_intent_reports_of_intent_from_graphdb(intent_id)

    if response.status_code != 200:
        return None

    results = response.json()["results"]["bindings"]

    if not results:
        return None

    intent_reports = []

    for r in results:
        id = r['report']["value"].split("/")[-1]

        intent_report = {
            "id": id,
            "agentName": r["agentName"]["value"],
            "response": r["response"]["value"],
            "creationDate": r["creationDate"]["value"],
            "executionTime": r["executionTime"]["value"]
        }
        intent_reports.append(intent_report)
    
    return intent_reports
    
def get_intent_report_of_intent(intent_id : str, report_id : str):
    """
    Function used to analyse the response of the database to get an intent report
    of an intent from their IDs and to format it.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    report_id : str
        The ID of the intent report.
    
    Returns
    -------
    intent_report : Dictionnary
        An intent report and its attributes.
    """
    
    if not select_intent_from_id(intent_id):
        return None
    
    response = repository.fetch_single_intent_report_from_graphdb(intent_id, report_id)

    if response.status_code != 200:
        return None

    result = response.json()["results"]["bindings"]

    if not result:
        return None

    intent_report_data = result[0]

    id = result[0]['report']["value"].split("/")[-1]

    intent_report = {
        "id": id,
        "agentName": intent_report_data["agentName"]["value"],
        "response": intent_report_data["response"]["value"],
        "creationDate": intent_report_data["creationDate"]["value"],
        "executionTime": intent_report_data["executionTime"]["value"]
    }
    
    return intent_report


def create_intent(author : str, content : str):
    """
    Function used to create a new intent and its associated intent report.

    Parameters
    ----------
    author : str
        The author of the intent.
    content : str
        The content of the intent.
    
    Returns
    -------
    Dictionnary
        A dictionnary containing the intent and its intent report.
    """
    
    intent_id = uuid.uuid4()
    creation_date = dt.datetime.now(dt.timezone.utc).isoformat()

    # Cleaning of the author name
    author_without_space = author.replace(" ", "_")
    
    response = repository.insert_intent_into_graphdb(intent_id, author_without_space, content, creation_date)
    
    if response.status_code not in {200, 201, 202, 204}:
        return None

    intent = select_intent_from_id(intent_id)
    
    report = create_intent_report(intent_id, content)

    if not intent or not report:
        return None
    
    return { "intent": intent, "intent_report": report }

def create_intent_report(intent_id : str, content : str):
    """
    Function used to call the agent with the content of the author and create an intent
    report with the response.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    content : str
        The content of the intent.

    Returns
    -------
    intent_report : Dictionnary
        An intent report and its attributes.
    """
    startTime = time.time()

    report_id_response = uuid.uuid4()
    creation_date = dt.datetime.now(dt.timezone.utc).isoformat()

    chat_result = custom_chat(content)

    result_extracted = moderator.initiate_chat(
        recipient= result_extractor,
        message= chat_result,
        max_turns= 1,
        summary_method= "last_msg"
    )

    result = result_extracted.summary
    
    # Cleaning the response of the agent
    result = result.replace('\\', '\\\\')
    result = result.replace('"', '\\"')
    result = result.replace('\n', '\\n')

    response = repository.insert_report_into_graphdb(report_id_response, intent_id, result_extractor.name, result, (time.time() - startTime), creation_date)

    if response.status_code not in {200, 201, 202, 204}:
        return None
    
    startTime = time.time()

    report_id_summary = uuid.uuid4()
    creation_date = dt.datetime.now(dt.timezone.utc).isoformat()

    summary_extracted = moderator.initiate_chat(
        recipient= summary_extractor,
        message= chat_result,
        max_turns= 1,
        summary_method= "last_msg"
    )

    summary = summary_extracted.summary

    # Cleaning the summary of the agent
    summary = summary.replace('\\', '\\\\')
    summary = summary.replace('"', '\\"')
    summary = summary.replace('\n', '\\n')
    
    response = repository.insert_report_into_graphdb(report_id_summary, intent_id, summary_extractor.name, summary, (time.time() - startTime), creation_date)

    if response.status_code not in {200, 201, 202, 204}:
        return None

    intent_report_response = get_intent_report_of_intent(intent_id, report_id_response)
    intent_report_summary = get_intent_report_of_intent(intent_id, report_id_summary)

    intent_report = {
        "response": intent_report_response,
        "summary": intent_report_summary
    }

    return intent_report

def update_partially_intent(intent_id : str, content : str):
    """
    Function used to update the content of an existing intent and create a new intent report.

    Parameters
    ----------
    author : str
        The author of the intent.
    content : str
        The content of the intent.
    
    Returns
    -------
    Dictionnary
        A dictionnary containing the modified intent and its new intent report.
    """
    if not select_intent_from_id(intent_id):
        return None
    
    update_date = dt.datetime.now(dt.timezone.utc).isoformat()
    
    update_response = repository.update_intent_content_from_graphdb(intent_id, content, update_date)

    if update_response.status_code not in {200, 201, 202, 204}:
        return None
    
    intent_report = create_intent_report(intent_id, content)

    if not intent_report:
        return None
    
    intent = select_intent_from_id(intent_id)
    
    return { "intent": intent, "intent_report": intent_report }

def delete_intent_from_id(intent_id : str):
    """
    Function used to delete an intent from its ID and all its intent reports.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.

    Returns
    -------
    bool
        Statement that the intent has been deleted.
    """
    if not select_intent_from_id(intent_id):
        return False
    
    delete_reports_response = repository.delete_reports_of_intent_from_graphdb(intent_id)

    if delete_reports_response.status_code not in {200, 201, 202, 204}:
        return False
    
    delete_intent_response = repository.delete_intent_from_graphdb(intent_id)

    if delete_intent_response.status_code not in {200, 201, 202, 204}:
        return False
    
    return True

def delete_report_from_id(intent_id : str, report_id : str):
    """
    Function used to delete an intent report from its ID and the intent ID.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    report_id : str
        The ID of the intent report.

    Returns
    -------
    bool
        Statement that the intent report has been deleted.
    """
    if not select_intent_from_id(intent_id):
        return False
    
    if not get_intent_report_of_intent(intent_id, report_id):
        return False
    
    response = repository.delete_report_of_intent_from_graphdb(intent_id, report_id)

    if response.status_code not in {200, 201, 202, 204}:
        return False
    
    return True
    
