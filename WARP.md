# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**inSwitch** translates high-abstraction-level stakeholder intents into concrete technical intents for INTEND tools or external intent-based management systems. It's a multi-agent system built with AutoGen that bridges the gap between business requirements and technical API invocations, specifically designed for the FILL use case within the EU Horizon Europe INTEND project.

The system uses LLM-powered agents to:
- Extract knowledge from documents and knowledge graphs
- Translate natural language intents into API calls (TMF921 v5 Intent Management API)
- Query RDF knowledge graphs using SPARQL
- Perform RAG (Retrieval-Augmented Generation) on technical documentation

## Development Environment

### Setup
This project uses **VS Code with devcontainers** (required Docker). Open the workspace in VS Code, and reopen in container when prompted, or use `Cmd+Shift+P` → "Dev Containers: Reopen in Container".

Inside the container:
- Install Python extension (ms-python.python)
- Install Jupyter extension (ms-toolsai.jupyter)
- Verify you're in the container by checking the terminal (user/node name should differ from host)

### Python Environment
Select the "base (Python 3.12.7)" kernel for Jupyter notebooks (path: `/opt/conda/bin/python`). If scripts fail to run, set this as the Python Interpreter via `Cmd+Shift+P` → "Python: Select Interpreter".

### Required Credentials
OpenAI API token must be stored in `./openai.credential` at the repository root. This file is gitignored.

## Running Code

**Primary execution method**: Jupyter Notebooks
- Most examples and demos are in `.ipynb` files
- Select the "base (Python 3.12.7)" kernel when opening notebooks
- Main notebooks are located in:
  - `usecases/fill/nb/` - FILL use case implementations
  - `inswitch/nerve_rag/` - RAG system examples
  - `playground/` - Experimental and test notebooks

**Example execution**: See `usecases/fill/doc/snapshots/Step1-simplied-doc-api-call-2024-11-15.ipynb` for a working example of intent translation.

## Code Architecture

### Core Components (`inswitch/`)

**Agent System** (`inswitch/agent/`)
- `basic.py` - Foundation agent factories using AutoGen's ConversableAgent:
  - `get_chat_agent()` - Interactive conversational agent with LLM
  - `get_llm_agent()` - Pure LLM agent for reasoning tasks
  - `get_fixed_reply_agent()` - Deterministic response agent
  - `get_tool_executor_agent()` - Agent for executing function calls
  
- `apiagent.py` - ApiAgent wraps LLM reasoning with function calling capabilities. Uses nested chats to delegate API function selection/invocation to an internal "driver" agent.

- `ragagent.py` - RagAgent extends AutoGen's RetrieveUserProxyAgent for document retrieval:
  - Integrates ChromaDB for vector storage
  - Uses OpenAI embeddings for semantic search
  - Supports custom document paths (local files or URLs)
  - `retrieve_docs()` method for querying document collections

- `rdf.py` - RdfAgent queries RDF knowledge graphs via SPARQL:
  - Accepts RDF file paths or rdflib Graph objects
  - Auto-generates sample KG context for the LLM
  - Provides `query_kg()` for executing SPARQL queries
  - `register_fixed_query()` allows pre-defined SPARQL query functions
  - LLM generates SPARQL dynamically when needed

- `filteragent.py` - FilterAgent determines if input contains specific tasks (used for routing/classification)

**LLM Configuration** (`inswitch/llm/`)
- `model.py` - Centralized OpenAI configuration:
  - `get_openai_model_config(model='gpt-4o')` - Returns API key and model name
  - Reads credentials from `./openai.credential`

**Utilities** (`inswitch/util.py`)
- `second_last_msg()` - Helper for extracting conversation history (used in summary methods)

### Agent Interaction Patterns

**Nested Chats**: Agents use AutoGen's nested chat feature to delegate work to internal "driver" agents (e.g., ApiAgent → api_caller, RagAgent → rag_caller). The parent agent receives requests, triggers nested chat with specialized sub-agent, and returns the summary.

**Function Registration**: All specialized agents (API, RAG, RDF) use AutoGen's `register_function()` to expose capabilities:
- `caller` - The LLM agent that decides when to call the function
- `executor` - The agent that actually executes the function
- This separation allows LLM-driven function selection with safe execution

### Use Cases (`usecases/`)

**FILL Use Case** (`usecases/fill/`)
- `filluc/` - FILL-specific components and mock services
- `nb/` - Jupyter notebooks demonstrating intent translation workflows:
  - `simple-api-rag.ipynb` - RAG + API invocation
  - `simple-complete-without-rag.ipynb` - Direct intent to API translation
  - `simple-kg-rag.ipynb` - Knowledge graph retrieval approaches
- `data/` - FILL-specific knowledge bases and documents
- `mcp/` - Multi-agent configuration and orchestration
- See `usecases/fill/README.md` for milestone progress and examples

### Experimental Code (`playground/`)
- Test scripts and notebooks for prototyping
- `fill-kg-nt.txt` / `fill-kg-tri.txt` - Sample RDF knowledge graph data
- Not intended for production use

## Key Dependencies

From `.devcontainer/requirements.txt`:
- `pyautogen==0.4.1` - Core multi-agent framework (note: also uses `autogen-agentchat~=0.2` for retrieval features)
- `neo4j==5.25.0` - Graph database client (currently unused, Neo4j service commented out in docker-compose)
- `chromadb<=0.5.0` - Vector database for RAG
- `rdflib==7.1.1` - RDF graph parsing and SPARQL queries
- `flaml[automl]~=2.3` - AutoML utilities

## TMF921 Intent Management API

The project implements TMF Forum's Intent Management API (v5). Related repository: https://github.com/baptisterambour/intent-back (currently being merged). Spec: https://www.tmforum.org/oda/open-apis/directory/intent-management-api-TMF921/v5.0

## Working with Agents

When creating new agents:
1. Inherit from ConversableAgent or use factory functions in `basic.py`
2. Set up nested chats if the agent needs internal reasoning steps
3. Register functions with clear descriptions for LLM function calling
4. Use `max_internal_turns` to limit nested conversation depth
5. Choose appropriate summary methods (`last_msg`, `reflection_with_llm`, or custom)

When debugging agent interactions:
- Check `agent.chat_messages` to inspect conversation history
- Verify LLM config includes valid OpenAI credentials
- Use `code_execution_config=False` to prevent unexpected code execution
- Set `human_input_mode='NEVER'` for fully automated agents

## Database Services (Currently Disabled)

The docker-compose.yml includes commented-out services for:
- **Neo4j** (ports 7475:7474, 7688:7687) - Graph database with APOC plugins
- **Fuseki** (port 3030) - Apache Jena SPARQL server

These can be enabled by uncommenting the relevant sections in `.devcontainer/docker-compose.yml` if needed for advanced knowledge graph operations.
