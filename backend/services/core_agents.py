# CORE AGENTS
# Contains the main agents used in the system

from inswitch.agent.basic import get_chat_agent, get_fixed_reply_agent

result_extractor = get_chat_agent(
    name = "result_extractor",
    system_message="""
        You will receive a transcript of message exchanges between multiple agents.
        Your job is to generate a clear and structured summary of what has been deployed and what the deployment included.
        Start by stating the name of the agent who made the final deployment decision.
        Do not paraphrase or analyze.
        Do not infer meaning or goals beyond what was said.
        Stick strictly to the content of the transcript.
    """
)

summary_extractor = get_chat_agent(
    name = "summary_extractor",
    system_message="""
        You will receive transcripts of conversations between multiple agents.

        Your job is to extract the summary of the final decision made by the target agent in each conversation with each agents.

        Do not paraphrase or analyze.
        Do not infer meaning or goals beyond what was said.

        Format your output like this:
        Conversation [#]:
            Agent: [name]
            Decision: "[summary]"
    """
)

moderator = get_fixed_reply_agent(
    name="moderator",
    reply = ""
)