# REPOSITORY
# Handles access to the database

import requests

def fetch_intents_from_graphdb():
    """
    Function used to get all of the intent stored in the database.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = """
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?id ?authorName ?content ?creationDate ?lastUpdate
    WHERE {
        ?intent a icm:Intent ;
        ex:author ?author ;
        ex:content ?content ;
        dcterms:created ?creationDate ;
        dcterms:modified ?lastUpdate .
        ?author foaf:name ?authorName .
        BIND(STR(?intent) AS ?id)
    }
    ORDER BY ASC(?creationDate)
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db",
        data={"query": sparql_query},
        headers={"Accept": "application/sparql-results+json"}
    )
    
    return response


def insert_intent_into_graphdb(intent_id : str, author : str, content : str, creation_date : str):
    """
    Function used to insert a new intent in the database.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    author : str
        The author of the intent.
    content : str
        The content of the intent.
    creation_date : str
        The date the intent has been made.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        ex:{intent_id} a icm:Intent ;
            ex:author <http://example.com/intent/person/{author}> ;
            ex:content "{content}" ;
            dcterms:created "{creation_date}"^^xsd:dateTime ;
            dcterms:modified "{creation_date}"^^xsd:dateTime .

        <http://example.com/intent/person/{author}> a foaf:Person ;
            foaf:name "{author}" .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query,
        headers={"Content-Type": "application/sparql-update"}
    )

    return response

def insert_report_into_graphdb(report_id : str, intent_id : str, agent_name : str, agent_response : str, response_time : str, creation_date : str):
    """
    Function used to insert a new intent report in the database.

    Parameters
    ----------
    report_id : str
        The ID of the intent report.
    intent_id : str
        The ID of the intent.
    agent_name : str
        The name of the agent who handled the intent.
    agent_response : str
        The response that gave the agent.
    response_time : str
        The execution time of the handle of the intent.
    creation_date : str
        The creation date of the intent report.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        <http://example.com/intent/{intent_id}/intentReport/{report_id}> a icm:IntentReport ;
            dcterms:created "{creation_date}"^^xsd:dateTime ;
            ex:agentName "{agent_name}" ;
            ex:executionTime "{response_time}"^^xsd:float ;
            ex:intent <http://example.com/intent/{intent_id}> ;
            ex:response "{agent_response}" .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query.encode("utf-8"),
        headers={"Content-Type": "application/sparql-update"}
    )

    return response

def select_intent_from_graphdb(intent_id : str):
    """
    Function use to get an intent from its ID.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """
    
    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?id ?authorName ?content ?creationDate ?lastUpdate
    WHERE {{
        BIND(<http://example.com/intent/{intent_id}> AS ?intent)
        ?intent a icm:Intent ;
        ex:author ?author ;
        ex:content ?content ;
        dcterms:created ?creationDate ;
        dcterms:modified ?lastUpdate .
        ?author foaf:name ?authorName .
        BIND(STR(?intent) AS ?id)
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db",
        data=sparql_query.encode("utf-8"),
        headers={
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json"
        }
    )
    
    return response

def fetch_intent_reports_of_intent_from_graphdb(intent_id : str):
    """
    Function used to get all of the intent reports of an intent, stored in the database.
    
    Parameters
    ----------
    intent_id : str
        The ID of the intent.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """
    
    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT ?report ?creationDate ?agentName ?response ?executionTime
    WHERE {{
        ?report a icm:IntentReport ;
                dcterms:created ?creationDate ;
                ex:agentName ?agentName ;
                ex:response ?response ;
                ex:executionTime ?executionTime ;
                ex:intent <http://example.com/intent/{intent_id}> .
    }}
    ORDER BY ASC(?creationDate)
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db",
        data=sparql_query.encode("utf-8"),
        headers={
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json"
        }
    )

    return response

def fetch_single_intent_report_from_graphdb(intent_id : str, report_id : str):
    """
    Function use to get an intent report of an intent, from their IDs.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    report_id : str
        The ID of the intent report.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX icm: <http://tio.models.tmforum.org/tio/v3.6.0/IntentCommonModel/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT ?report ?creationDate ?agentName ?response ?executionTime
    WHERE {{
        BIND(<http://example.com/intent/{intent_id}/intentReport/{report_id}> AS ?report)
        ?report a icm:IntentReport ;
            dcterms:created ?creationDate ;
            ex:agentName ?agentName ;
            ex:response ?response ;
            ex:executionTime ?executionTime ;
            ex:intent <http://example.com/intent/{intent_id}> .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db",
        data=sparql_query.encode("utf-8"),
        headers={
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json"
        }
    )

    return response


def update_intent_content_from_graphdb(intent_id : str, new_content : str, update_date : str):
    """
    Function used to update the content of an intent from its ID.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    new_content : str
        The new content of the intent.
    update_date : str
        The date the intent has been updated.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    DELETE {{
        <http://example.com/intent/{intent_id}> ex:content ?oldContent .
        <http://example.com/intent/{intent_id}> dcterms:modified ?oldDate .
    }}
    INSERT {{
        <http://example.com/intent/{intent_id}> ex:content "{new_content}" .
        <http://example.com/intent/{intent_id}> dcterms:modified "{update_date}"^^xsd:dateTime .
    }}
    WHERE {{
        <http://example.com/intent/{intent_id}> ex:content ?oldContent .
        OPTIONAL {{ <http://example.com/intent/{intent_id}> dcterms:modified ?oldDate . }}
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query.encode("utf-8"),
        headers={"Content-Type": "application/sparql-update"}
    )

    return response


def delete_intent_from_graphdb(intent_id : str):
    """
    Function used to delete an intent from its ID.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    DELETE {{
        <http://example.com/intent/{intent_id}> ?p ?o .
    }}
    WHERE {{
        <http://example.com/intent/{intent_id}> ?p ?o .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query.encode("utf-8"),
        headers={"Content-Type": "application/sparql-update"}
    )
    
    return response

def delete_reports_of_intent_from_graphdb(intent_id : str):
    """
    Function used to delete all intent reports of an intent.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """

    # QUERY
    sparql_query = f"""
    PREFIX ex: <http://example.com/intent/>

    DELETE {{
        ?report ?p ?o .
    }}
    WHERE {{
        ?report ex:intent <http://example.com/intent/{intent_id}> .
        ?report ?p ?o .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query.encode("utf-8"),
        headers={"Content-Type": "application/sparql-update"}
    )
    
    return response

def delete_report_of_intent_from_graphdb(intent_id : str, report_id : str):
    """
    Function used to delete an intent report of an intent, from their IDs.

    Parameters
    ----------
    intent_id : str
        The ID of the intent.
    report_id : str
        The ID of the intent report.

    Returns
    -------
    requests.Response
        Response object containing the results of the SPARQL query in JSON format.
    """
    
    # QUERY
    sparql_query = f"""
    DELETE {{
        <http://example.com/intent/{intent_id}/intentReport/{report_id}> ?p ?o .
    }}
    WHERE {{
        <http://example.com/intent/{intent_id}/intentReport/{report_id}> ?p ?o .
    }}
    """

    response = requests.post(
        "http://graphdb:7200/repositories/intent-db/statements",
        data=sparql_query.encode("utf-8"),
        headers={"Content-Type": "application/sparql-update"}
    )

    return response
