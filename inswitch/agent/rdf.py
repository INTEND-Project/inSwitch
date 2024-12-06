from autogen import ConversableAgent, register_function
from inswitch.agent.basic import get_chat_agent, get_llm_agent, get_tool_executor_agent
from typing import List, Callable, Any, Union
from rdflib import Graph, URIRef
from functools import wraps
from typing import Any

RDF_CALLER_DEFAULT_SYSTEM_MESSAGE = '''
You have access to a knowledge graph via a group of function that extract knowledge from the graph.
If none of the functions fit what you want to extract, you can use the default function to run
a SPARQL query that you generate from scratch. 
When you generate SPARQL to query triples with a known subject, predict or object,
try to use the filter clause.
For example: SELECT ?subject ?predict ?object WHERE{?subject ?predict ?object FILTER(?subject = a:subject)},
or WHERE{?subject ?predict ?object FILTER(?predict = a:predict)}
'''




class RdfAgent(ConversableAgent):
    def __init__(self, name:str, graph: Union[str, Graph], system_message: str = "", max_internal_turns = 1):
        super().__init__(
            name,
            llm_config=False,
            code_execution_config=False
        )
        if isinstance(graph, str):
            self.kg = Graph()
            self.kg.parse(graph)
        else:
            self.kg = graph

        samplekg = self.get_sample_kg()
        prefix = self.get_namespaces(samplekg)
        
        self.caller_system_message = f"{RDF_CALLER_DEFAULT_SYSTEM_MESSAGE} {system_message}"
        self.rdf_caller = get_llm_agent(
            f'{name}_driver', 
            system_message=f"{self.caller_system_message}\n Sample Knowledge Graph for reference: \n{samplekg}\n Namespaces:\n{prefix}"
        )
        self.register_nested_chats(
            [
                {
                    "recipient": self.rdf_caller,
                    "max_turns": max_internal_turns,
                    "summary_method": 'last_msg'
                }
            ],
            trigger = lambda sender: sender not in [self.rdf_caller]
        )

        def query_kg_with_sparql(query:str)->str:
            return self.query_kg(query)

        register_function(
            f=query_kg_with_sparql, 
            caller=self.rdf_caller, 
            executor=self, 
            description="This is the function to query subgraph. The input is a SPARQL query and the output is a string with all the tripples"
        )
    
    
    def query_kg(self, query:str)->str:
        skg = self.kg.query(query)
        result = ""
        for row in skg:
            # Use namespace_manager to abbreviate URIs
            row_result = ""
            for item in row:
                item_prefix = self.kg.namespace_manager.qname(item) if isinstance(item, URIRef) else f'"{item}"'
                row_result = f"{row_result} {item_prefix}" 
            result = f"{result}\n{row_result}"
        return result

    def get_sample_kg(self)->str:
        return self.query_kg("""
            SELECT (SAMPLE(?subject) AS ?sampleSubject) ?predicate  (SAMPLE(?object) AS ?sampleObject)
            WHERE {
            ?subject ?predicate ?object .
            }
            GROUP BY ?predicate
        """)

    def get_namespaces(self, samplekg:str)->str:

        return "\n".join(
            f"@Prefix {prefix}: {namespace}" 
            for prefix, namespace in self.kg.namespace_manager.namespaces()
            if prefix+':' in samplekg
        )

    def register_fixed_query(self, func:Callable, description):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            query = func(*args, **kwargs)
            return self.query_kg(query)

        wrapper.__name__ = func.__name__ +"_exec"

        register_function(
            f=wrapper, 
            caller=self.rdf_caller, 
            executor=self, 
            description= description
        )

