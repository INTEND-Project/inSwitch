from inswitch.llm.model import get_openai_model_config
from autogen import ConversableAgent

def get_chat_agent(name: str, system_message = "you are a helpful assistant")->ConversableAgent:

    return ConversableAgent(
        name,
        system_message = system_message,
        llm_config = {"config_list": [get_openai_model_config()]},
        code_execution_config=False,  # Turn off code execution for this agent.
    )

def get_fixed_reply_agent(name: str, reply: str) -> ConversableAgent:
    return ConversableAgent(
        name,
        llm_config = False, 
        default_auto_reply = reply,
        code_execution_config = False,
        human_input_mode = 'NEVER'
    )

def get_llm_agent(name: str, system_message = "You are a helpful assistant") -> ConversableAgent:
    return ConversableAgent(
        name,
        system_message = system_message,
        llm_config = {"config_list": [get_openai_model_config()]},
        code_execution_config=False,  # Turn off code execution for this agent. 
    )

def get_tool_executor_agent(name: str) -> ConversableAgent:
    return ConversableAgent(
        name,
        llm_config=False,
        code_execution_config=False,
        human_input_mode='NEVER'
    )

if __name__ == "__main__":
    print(get_openai_model_config('gpt-4o'))