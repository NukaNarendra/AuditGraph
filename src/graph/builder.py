from src.graph.neo4j_client import Neo4jClient
from src.graph.schema import GraphData


class GraphBuilder:
    def __init__(self):
        self.client = Neo4jClient()

    def push_to_neo4j(self, data: GraphData):
        if not data.entities:
            return

        print(f"   Ingesting {len(data.entities)} nodes and {len(data.relationships)} edges...")

        # 1. Merge Entities (Nodes)
        for entity in data.entities:
            query = f"""
            MERGE (e:{entity.type} {{id: $id}})
            SET e += $props
            """
            self.client.query(query, {"id": entity.id, "props": entity.properties})


        for rel in data.relationships:

            rel_type = rel.type.upper().replace(" ", "_")

            query = f"""
            MATCH (a {{id: $source_id}}), (b {{id: $target_id}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r += $props
            """
            self.client.query(query, {
                "source_id": rel.source,
                "target_id": rel.target,
                "props": rel.properties
            })