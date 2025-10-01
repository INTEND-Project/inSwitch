# Running the single agent MCP Server
The MCP server was tested with the setup [here](https://modelcontextprotocol.io/docs/develop/build-server#python) on Windows with the mcp[cli] and rdflib libraries with the free version of Claude for Desktop as the MCP client.
We added a "fill" MCP server in claude_desktop_config.json which can be found in Claude for Desktop settings, Developer, Edit Config.
The intent we tested with was "I am a customer and own Machine4. I want to add a new service to my machine to record all the alarms."
If the MCP server was set up correctly the two tools get_service_desc and find_containers should be called in sequential order.
