# inSwitch
LLM agents for context switching from business-level intents to resource-level intents in the cognitive computing continuum.  
More information for the INTEND project that inSwitch is part of can be found [here](https://intendproject.eu/).

# Install
We recommend using [VS Code + devcontainer](https://code.visualstudio.com/docs/devcontainers/containers). You need to install the devcontainers extension to VS Code. After that, when you open this workspace in Code, there will be a pop-up window asking if you want to re-open it in devcontainer. If you missed it, use cmd+shift+p, and select 
"Dev Containers: Reopen in Container". Make sure you have a docker environment running. 

Once the workspace is reopened inside a container (to make sure it is inside a container, launch a terminal and check the user name and node name), you may need to manually install two extensions to the "new VS code", i.e., Python (ms-python.python) and Jupyter (ms-toolsai.jupyter).

You need a valid token for OpenAI API, stored in ./openai.credential. Other LLM models will be supported later. 

# Structure
- [./inswitch](inswitch/): generic components for inSwitch
- [./usecases](usecases/): data, scripts, components, etc., for different use cases

# Run
Most of the running examples and demos are in Jupyter Notebooks. To run them, you need to select a kernal - choose a python environment called "base (Python 3.12.7)". The version may vary. It is the under path "/opt/conda/bin/python".

If you face problem running python scripts, you may also try to select this same "base" python as the Python Interpreter (this can be done also via cmd+shift+p).

# Use cases
All the use cases can be found in [usecase](./usecases/). Four each use case, there is a README.md file for further information.

# First taste
So far, we have one simplified example running. You can check the snapshot [here](./usecases/fill/doc/snapshots/Step1-simplied-doc-api-call-2024-11-15.ipynb)

# Development plan
