from rdflib import Graph, URIRef
from rdflib.namespace import split_uri
# Create a Graph
g = Graph()

# Parse in an RDF file hosted on the Internet
g.parse("./usecases/fill/data/anonimized_data_fill.ttl")

sg = g.query("""
SELECT (SAMPLE(?subject) AS ?sampleSubject) ?predicate  (SAMPLE(?object) AS ?sampleObject)
WHERE {
  ?subject ?predicate ?object .
}
GROUP BY ?predicate
""")

# for row in g:
#     print(row)

def localname(uri):

    # Check if it's a URIRef and split to get the local name
    if isinstance(uri, URIRef):
        try:
            return split_uri(uri)[1]
        except ValueError:
            # If split_uri fails, fallback to manual split
            return uri.split('/')[-1] if '/' in uri else uri
    return uri  # Return as is if it's not a URIRef

# Print triples in the desired format
for s, p, o in sg:
    # Use namespace_manager to abbreviate URIs
    subject_prefix = g.namespace_manager.qname(s)
    predicate_prefix = g.namespace_manager.qname(p)
    object_prefix = g.namespace_manager.qname(o) if isinstance(o, URIRef) else f'"{o}"'
    
    # Print in the desired format
    print(f"{subject_prefix} {predicate_prefix} {object_prefix}")
# for subj, pred, obj in g:
#     print(f"{localname(subj)} {localname(pred)} {localname(obj)}")
    

# # Loop through each triple in the graph (subj, pred, obj)
# for subj, pred, obj in g:
#     # Check if there is at least one triple in the Graph
#     if (subj, pred, obj) not in g:
#        raise Exception("It better be!")

# # Print the number of "triples" in the Graph
# print(f"Graph g has {len(g)} statements.")
# # Prints: Graph g has 86 statements.

# for subj, pred, obj in g:
#     print(f"{subj} {pred} {obj}")