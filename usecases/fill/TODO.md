# A list of tasks to be done before a running example

1. First running example without RAG (Done)
    - Who: Hui
2. Knowledge graph RAG
    - *Who*? David and Becca
    - Depedency: need a complete knowledge graph for FILL from URO
    1. Basic functions manuplate a tripple store
        - starting from rdflib?
        - (later) fuseki or other permenat tripple stores
        - SPARQL query -> rewrite the result into simple (more natural) triples
    2. A tool-executor agent to wrap the functions
    3. A two-agent system with tool driver and tool executor
        - tool driver: get input text, generate SPARQL query
        - tool executor: run the query, return tripples
        - tool driver: return the query
    4. Nested agent to wrap up the KG RAG function
    
3. Document RAG
    - *Who*? Adela
    - Preparation: Extract the API document for Nerve: https://docs.nerve.cloud/developer_guide/dna/.
      - Question: Is it possible to directly use the links to the HMTL pages?
    1. (To decide) Should we use autogen's [RAG assistant](https://microsoft.github.io/autogen/0.2/blog/2023/10/18/RetrieveChat/), or a simple tool wrapping up a vector database?
    2. Select the encoding the model, and size of the trunks
    3. Demo of query: "I want deploy some workloads into my machine, which API should I use" -> document excerpts about the Nerve DNA API (challenge: there are other APIs about "deployment"...)
    4. Nested agent to wrap up the doc RAG function

4. API-based real-time RAG
    - **Who** Hui
    - Preparation: mock-up APIs for querying what workloads are available and get their hash codes.
    - Tool agents to call the API on demand
    - Tool drivers -> call API to check workload availability -> feedback for missing of workloads -> call API to deploy workloads
    - Nested agent to call the API

5. Some common structures into the generic inSwitch [code](../../inswitch/)
    - **who**
    - simple agents: fixed reply (done), simple chat (done)
    - sequences: one talking to the next, control carryover
    - nested agent
    - tool agent
5. Integration and demo
    - **who?**


