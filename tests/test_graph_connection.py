import sys
import os

# Add the project root to the python path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph.neo4j_client import Neo4jClient


def test_neo4j_connection():
    print("🔌 Testing Neo4j Connection...")

    try:
        # 1. Initialize Client
        client = Neo4jClient()

        # 2. Run a simple 'Ping' query
        result = client.query("RETURN 'Connection Successful' AS status")

        # 3. Verify Result
        if result and result[0]['status'] == 'Connection Successful':
            print(" SUCCESS: Connected to Neo4j Database!")

            # Optional: Check if we have data
            count = client.query("MATCH (n) RETURN count(n) as count")
            print(f"Current Database Stats: {count[0]['count']} nodes found.")

        else:
            print(" FAILURE: Connected but received unexpected result.")

        client.close()

    except Exception as e:
        print("\n CRITICAL FAILURE: Could not connect to Neo4j.")
        print(f"   Error Details: {e}")
        print("\n   Troubleshooting Checklist:")
        print("   1. Is Docker running? (Run 'docker ps')")
        print("   2. Did you run 'docker-compose up'?")
        print("   3. Check .env file for correct password (default: password)")


if __name__ == "__main__":
    test_neo4j_connection()