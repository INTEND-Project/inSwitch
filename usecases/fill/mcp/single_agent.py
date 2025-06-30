from mcp.server.fastmcp import FastMCP
from rdflib import Graph
from rdflib import URIRef

mcp = FastMCP("fill")

kg = Graph()
kg.parse("FILL__KG_anon_services.jsonld")

@mcp.tool()
def get_service_desc() -> str:
    """Get service descriptions."""
    
    select_query = """
    PREFIX intend: <https://intendproject.eu/schema/>

    SELECT ?description WHERE {    
        ?service intend:description ?description
    }
    """
    qres = kg.query(select_query)
    triples = []
    for row in qres:
        triples.append( str(row[0]))
    return '\n'.join(triples)

# print( get_service_desc())

@mcp.tool()
def find_containers(
        machine: str,
        service: str
    ) -> str:
    """Find containers needed to deploy service.
    
    Args:
        machine: machine that customer owns
        service: service to deploy
    """
    
    machine = "fill:" + machine
    service = "fill:" + service
    select_query = f"""
    PREFIX fill: <https://intendproject.eu/fill/>
    PREFIX intend: <https://intendproject.eu/schema/>

    SELECT ?container WHERE {{
        {machine} intend:hasService ?service FILTER(?service = {service})
        ?service intend:hasComponent ?component .
        ?component intend:hasContainer ?container .
        ?container intend:canBeDeployedOn {machine} .
    }}
    """

    qres = kg.query(select_query)
    containers = []
    if qres:
        for row in qres:
            containers.append(row[0].replace('https://intendproject.eu/fill/',''))
        return ', '.join(containers)
    else:
        return "Can't find containers."

# print( find_containers('Machine4', 'Service5'))
mcp.run(transport='stdio')