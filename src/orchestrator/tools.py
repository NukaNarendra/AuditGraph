from langchain_core.tools import tool
from src.graph.neo4j_client import Neo4jClient
from src.analysis.fraud_rules import FraudRules

# Initialize DB Client once for tools
db_client = Neo4jClient()


@tool
def run_audit_query(query_type: str):
    """
    Executes a specific forensic audit rule.
    Valid `query_type` inputs:
    - 'related_party': Checks for conflicts of interest (employee-owned vendors).
    - 'circular_flow': Checks for round-tripping money.
    - 'unverified_vendor': Checks for large payments without contracts.
    """
    print(f"🛠️ Tool Triggered: Running {query_type} check...")

    if query_type == "related_party":
        cypher = FraudRules.get_undisclosed_related_party_query()
    elif query_type == "circular_flow":
        cypher = FraudRules.get_circular_flow_query()
    elif query_type == "unverified_vendor":
        cypher = FraudRules.get_high_value_unknown_vendor_query()
    else:
        return "Invalid query type. Available: related_party, circular_flow, unverified_vendor"

    try:
        results = db_client.query(cypher)
        if not results:
            return "No suspicious patterns found for this rule."
        return str(results)
    except Exception as e:
        return f"Database Error: {e}"


@tool
def run_custom_cypher(query: str):
    """
    Executes a raw Cypher query against the Neo4j database.
    Use this to explore relationships dynamically.
    Example: "MATCH (n:Person) RETURN n.id limit 5"
    """
    # Safety check (Basic injection prevention for MVP)
    if "DELETE" in query.upper() or "DETACH" in query.upper():
        return "Action Forbidden: Deletion is not allowed in Audit Mode."

    try:
        return str(db_client.query(query))
    except Exception as e:
        return f"Syntax Error in Cypher: {e}"