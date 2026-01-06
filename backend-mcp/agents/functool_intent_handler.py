
import asyncio

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
import requests

DECISION_TAG = "DECISION_JSON:"
DECISION_AGENT_SYSTEM_MESSAGE = (
    "You are an assistant agent that helps process user intents. "
    "You can use the provided tools to get external knowledge on handling intents."
    "Make your own plan and analyze the tool outputs."
    f"When you reach a final decision, such as which service to deply, output:\n"
    f"{DECISION_TAG} {{...json...}}\n"
    "Then output the word TERMINATE on its own line."
)

def query_sparql(query: str) -> str:
    endpoint = "http://graphdb:7200/repositories/system-dt"
    headers = {
        "Accept": "text/turtle",
        "Content-Type": "application/sparql-query"
    }
    response = requests.post(endpoint, data=query.encode("utf-8"), headers=headers)
    response.raise_for_status()
    return response.text

def get_namespaces() -> str:
    import requests
    repo = "system-dt"
    base = "http://graphdb:7200"
    url = f"{base}/repositories/{repo}/namespaces"

    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    ns = r.json()  # dict: { "rdf": "http://...", "ex": "http://..." }

    bindings = ns["results"]["bindings"]
    pairs = []
    for b in bindings:
        p = b["prefix"]["value"]
        ns = b["namespace"]["value"]
        pairs.append((p, ns))

    return "\n".join(f"PREFIX {p}: <{ns}>" for p, ns in sorted(pairs))

def get_meta_data() -> str:
    """
    Function to get the schema of the knowledge graph. It only shows how the data is structured, without
    providing the full data. You may use this as a reference to write SPARQL queries to get actual data.

    Returns
    -------
    str
        All the prefixes, followed by a sample triple for each predicate in the graph.
    """
    # Placeholder implementation

    prefix_block = get_namespaces()
    
    query = """
    CONSTRUCT {
        ?s ?p ?o .
    }
    WHERE {
        {
            SELECT ?p (SAMPLE(?s) AS ?s) (SAMPLE(?o) AS ?o)
            WHERE { ?s ?p ?o }
            GROUP BY ?p
        }
    }"""
    return query_sparql(f"{prefix_block} {query}")

def get_additional_info_of_system() -> str:
    """
    Function to get additional, human-friendly meta-data about the system digital twin. 
    Recommend to call it before deciding on making queries. This is only auxiliary information, 
    you still need to get the exact meta data or schema so that you can make correct SPARQL queries.

    Returns
    -------
    str
        Additional information about the system.
    """
    
    return """
    The system digital twin represents the available machine data analytics services for the machine tools.
    Each service has natural language descriptions, which may be blurred and use different terminology than the user. 
    Make sure to read all the descriptions to decide which one to use, instead of querying keywords from description test.
    A service may be composed of various components, which in term is composed of containers. 
    Not all containers work on all the machines, so check the compatibility information before deciding which component or container to deploy.
    """

def query_graph_db(sparql_query: str) -> str:
    """
    Function to query the system digital twin in the graph database using SPARQL. 
    This allows you to retrive part of the real data that is relevant to your decision making.
    Always use CONSTRUCT or DESCRIBE queries, 
    never SELECT! Remember to add prefixes. 
    Do NOT use CONTAIN or FILTER clauses, as descriptions are blurred and may use different terminology.

    Parameters
    ----------
    sparql_query : str
        The SPARQL query string. 

    Returns
    -------
    str
        Query results.
    """

    print(f"------- Executing SPARQL Query -------\n{sparql_query}\n-------------------------------")
    result = query_sparql(sparql_query)
    print(f"\n------- SPARQL Query Result -------\n{result}\n-------------------------------")
    return result



def extract_decision(messages) -> str:
    """
    Extract the last DECISION_JSON block from assistant messages.
    """
    for m in reversed(messages):
        content = getattr(m, "content", "") or ""
        if DECISION_TAG in content:
            # grab everything after the tag (same line or remainder)
            return content.split(DECISION_TAG, 1)[1].strip()
    raise ValueError("No decision found. Ensure the decision agent outputs DECISION_JSON: ...")


async def handle_intent(intent, create_intent_report):

    try:
        intent_id = intent.get("id", None)
        content = intent.get("content", None)

        if not intent_id or not content:
            raise ValueError("Intent must have 'id' and 'content' fields.")

        # Process the intent (business logic can be added here)


        with open("openai.credential", "r") as f:
            openai_api_key = f.read().strip() 
        model_client = OpenAIChatCompletionClient(
            model="gpt-5-mini",
            api_key=openai_api_key   
        )

        decision_maker = AssistantAgent(
            name="decision_maker",
            model_client=model_client,
            tools=[
                    get_meta_data, 
                    query_graph_db,
                    get_additional_info_of_system
                ],             # local function tool - will be replaced by MCP tools in the future.
            reflect_on_tool_use=True,             # have the model summarize/reflect on tool outputs
            system_message=DECISION_AGENT_SYSTEM_MESSAGE
        )

        decision_termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
        decision_team = RoundRobinGroupChat(
            participants=[decision_maker],
            termination_condition=decision_termination,
        )

        decision_result = await Console(decision_team.run_stream(task=content))
        decision_json_text = extract_decision(decision_result.messages)

        # Create an intent report if the flag is set
        if create_intent_report:
            report = create_intent_report(intent_id, f"I am tring to handle intent {intent_id} with content: {content}. And the decision is: {decision_json_text}")
            return {"status": "success", "report": report}
        else:
            return {"status": "success", "message": "Intent processed without report."}


    except Exception as e:
        return {"status": "error", "message": str(e)}





async def main():
    # Example usage
    intent = {
        "id": "intent_123",
        "content": "I need a service to record alarms of my machines"
    }

    def mock_create_intent_report(intent_id, message):
        print(message)
        return {
            "intent_id": intent_id,
            "message": message,
            "status": "created"
        }

    result = await handle_intent(intent, mock_create_intent_report)
    print(result)  

async def main_test_query():
    meta_data = get_meta_data()
    print("Meta Data:")
    print(meta_data) 



if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(main_test_query())
    # asyncio.run(main_test_query())