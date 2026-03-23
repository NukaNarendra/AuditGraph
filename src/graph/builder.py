from src.graph.neo4j_client import Neo4jClient


class GraphBuilder:
    def __init__(self):
        self.client = Neo4jClient()

    def push_to_neo4j(self, graph_data):
        """Takes our parsed dictionary and runs Cypher queries to build the graph."""

        # 1. Safely extract nodes and edges from the dictionary
        if not isinstance(graph_data, dict):
            print("   ⚠️ Error: Builder expected a dictionary.")
            return

        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])

        # 2. Ingest Nodes (People, Companies, etc.)
        for node in nodes:
            node_id = node.get("id")
            node_type = node.get("type", "Entity")

            if not node_id:
                continue

            # Clean the type to prevent Cypher syntax errors
            node_type = "".join(e for e in str(node_type) if e.isalnum())
            if not node_type:
                node_type = "Entity"

            # MERGE creates the node if it doesn't exist, or matches it if it does
            query = f"MERGE (n:`{node_type}` {{id: $id}})"
            try:
                self.client.query(query, {"id": str(node_id)})
            except Exception as e:
                print(f"      ⚠️ Failed to insert node {node_id}: {e}")

        # 3. Ingest Edges (Relationships)
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            rel_type = edge.get("type", "RELATED_TO")

            if not source or not target:
                continue

            # Clean the relationship type (must be uppercase, no spaces)
            rel_type = "".join(e for e in str(rel_type) if e.isalnum() or e == "_").upper()
            if not rel_type:
                rel_type = "RELATED_TO"

            # Check if there is an amount (for money transfers)
            props = edge.get("properties", {})
            amount = props.get("amount")

            try:
                if amount:
                    query = f"""
                    MATCH (s {{id: $source}})
                    MATCH (t {{id: $target}})
                    MERGE (s)-[r:`{rel_type}`]->(t)
                    SET r.amount = $amount
                    """
                    self.client.query(query, {"source": str(source), "target": str(target), "amount": str(amount)})
                else:
                    query = f"""
                    MATCH (s {{id: $source}})
                    MATCH (t {{id: $target}})
                    MERGE (s)-[r:`{rel_type}`]->(t)
                    """
                    self.client.query(query, {"source": str(source), "target": str(target)})
            except Exception as e:
                print(f"      ⚠️ Failed to insert edge {source} -> {target}: {e}")