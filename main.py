import time
from src.ingestion.loader import DataLoader
from src.ingestion.parser import DocumentParser
from src.graph.builder import GraphBuilder
from src.graph.neo4j_client import Neo4jClient


def main():
    print("===========================================")
    print("   AUDITGRAPH: AUTONOMOUS DILIGENCE")
    print("===========================================")

    loader = DataLoader()
    parser = DocumentParser()
    builder = GraphBuilder()

    try:
        builder.client.clear_database()
        print("Database cleared.")
    except Exception as e:
        print(f" Warning: Could not clear database: {e}")

    for filename, text in loader.load_documents():

        try:
            print(f"   Processing: {filename}...")

            graph_data = parser.extract_graph_from_text(text, filename)


            if graph_data.get("nodes") or graph_data.get("edges"):
                builder.push_to_neo4j(graph_data)
                print("   Success!")
            else:
                print("    No entities found to ingest.")

        except Exception as e:
            print(f"   Failed to process {filename}")
            print(f"      Error: {e}")

        print(" Cooling down for 20 seconds...")
        time.sleep(20)

    print("\n Ingestion Complete!")
    print(" Go to http://localhost:7474 to explore your Knowledge Graph.")

    print("\n Running Automatic Fraud Check...")
    suspicious_query = """
    MATCH (p:Person)-[:OWNS|DIRECTOR_OF]->(c:Company)
    MATCH (c)-[r:TRANSFERRED_MONEY]->(x)
    RETURN p.id as Person, c.id as Shell_Company, x.id as Recipient, r.amount as Amount
    LIMIT 5
    """

    try:
        results = builder.client.query(suspicious_query)
        if results:
            print(" FLAG DETECTED: Potential Related Party Transactions:")
            for r in results:
                print(r)
        else:
            print(" No obvious flags found yet. Check your Graph in Neo4j Browser!")
    except Exception as e:
        print(f"Query Error: {e}")


if __name__ == "__main__":
    main()