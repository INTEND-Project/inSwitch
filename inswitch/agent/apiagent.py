from autogen import ConversableAgent, register_function
from inswitch.agent.basic import get_chat_agent, get_llm_agent, get_tool_executor_agent
from typing import List, Callable, Any

TOOL_CALLER_DEFAULT_SYSTEM_MESSAGE = '''
You are a helpful assistant. 
You have access to some functions through which you can invoke an useful API.
When you get a task, you need to decide which functions to call, and how to call them.
You may also need to call it in several rounds.
'''

class ApiAgent(ConversableAgent):
    def __init__(self, name:str, system_message: str = "", max_internal_turns = 1):
        super().__init__(
            name,
            llm_config=False,
            code_execution_config=False
        )
        self.caller_system_message = f"{TOOL_CALLER_DEFAULT_SYSTEM_MESSAGE} {system_message}"
        self.api_caller = api_caller = get_llm_agent(f'{name}_driver', system_message=self.caller_system_message)
        self.register_nested_chats(
            [
                {
                    "recipient": api_caller,
                    "max_turns": max_internal_turns,
                    "summary_method": 'last_msg'
                }
            ],
            trigger = lambda sender: sender not in [api_caller]
        )
    
    def register_api_function(self, fun: Callable[..., Any], description: str = ""):
        register_function(
            f=fun, 
            caller=self.api_caller, 
            executor=self, 
            description=description
        )
        
