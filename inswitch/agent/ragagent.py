import sys
sys.path.append('../..')

from autogen import ConversableAgent, register_function, Agent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from inswitch.agent.basic import get_llm_agent
from typing import List, Callable, Any, Optional, Dict, Tuple, Union
from inswitch.llm.model import get_openai_model_config
from chromadb.utils import embedding_functions
import json


TOOL_CALLER_DEFAULT_SYSTEM_MESSAGE = '''
You're a repeating chatbot. You will be provided with retrieved documents and you will repeat these as output. Please do NOT change the content and do NOT give explanations."
'''

class RagAgent(RetrieveUserProxyAgent):
    def __init__(self, name:str, docs_path: List[str] = None, max_internal_turns = 1):
        super().__init__(
            name,
            llm_config=False,
            code_execution_config=False,
            human_input_mode="NEVER",
            retrieve_config={
                "task": "qa",
                "docs_path": docs_path,
                "model": get_openai_model_config()["model"],
                "embedding_function": embedding_functions.OpenAIEmbeddingFunction(api_key = get_openai_model_config()["api_key"]), # alternatively, "all-mpnet-base-v2"
                "get_or_create": True,  # set to False if you don't want to reuse an existing collection
                "chunk_token_size": self.get_max_tokens(get_openai_model_config()["model"]) * 0.1
            },
        )
        self.caller_system_message = f"{TOOL_CALLER_DEFAULT_SYSTEM_MESSAGE}"
        self.rag_caller = rag_caller = get_llm_agent(f'{name}_driver', system_message=self.caller_system_message)

        def reply_func(
                recipient: ConversableAgent,
                messages: Optional[List[Dict]] = None,
                sender: Optional[Agent] = None,
                config: Optional[Any] = None,
            ) -> Tuple[bool, Union[str, Dict, None]]:
            self.initiate_chat(
                self.rag_caller, 
                message=self.message_generator, 
                problem="I want to obtain API info for deploying docker workload with ID docker3.")
            return (True, self.retrieve_docs(problem = "I want to obtain info for the workload with ID docker3 and version 3 and hash 5454854754kcnvcl43.", n_results = 3))


        self.register_reply(
            trigger = lambda sender: sender not in [rag_caller],
            reply_func = reply_func
        )

        
    @staticmethod
    def message_generator(sender, recipient, context):
        """
        Generate an initial message with the given context for the RetrieveUserProxyAgent.
        Args:
            sender (Agent): the sender agent. It should be the instance of RetrieveUserProxyAgent.
            recipient (Agent): the recipient agent. Usually it's the assistant agent.
            context (dict): the context for the message generation. It should contain the following keys:
                - `problem` (str) - the problem to be solved.
                - `n_results` (int) - the number of results to be retrieved. Default is 20.
                - `search_string` (str) - only docs that contain an exact match of this string will be retrieved. Default is "".
        Returns:
            str: the generated message ready to be sent to the recipient agent.
        """
        sender._reset()
        problem = context.get("problem", "")
        n_results = context.get("n_results", 10)
        search_string = context.get("search_string", "")

        sender.retrieve_docs(problem, n_results, search_string)
        sender.problem = problem
        sender.n_results = n_results
        doc_contents = sender._get_context(sender._results)
        message = f"Retrieved Context: {doc_contents}"
        return message

    def register_rag_function(self, description: str = ""):
        def retrieve(task:str , n_results:int=2)-> str:
            """
            Retrieve documents for the given task and return the results as a JSON string.

            Parameters:
            - task (str): The task description or query for document retrieval.
            - n_results (int): The number of results to retrieve. Default is 2.

            Returns:
            - str: JSON string containing the retrieved documents.
            """
            self.retrieve_docs(problem = task, n_results = n_results)
            return json.dumps(self._results)
    
        register_function(
            f=retrieve, 
            caller=self.rag_caller, 
            executor=self, 
            description=description
        )

    
#ra = RagAgent("ra", docs_path = ["https://docs.nerve.cloud/developer_guide/dna/"])
#results = ra.retrieve(task = "Tell me about DNA")
#print(results)
