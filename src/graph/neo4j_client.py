from neo4j import GraphDatabase
from src.config import Config

class Neo4jClient:
    def __init__(self):

        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD),
            encrypted=False
        )

    def close(self):
        self.driver.close()

    def query(self, query: str, parameters=None):

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            print(f"❌ Query Failed: {e}")
            raise e

    def clear_database(self):

        self.query("MATCH (n) DETACH DELETE n")
        print(" Database cleared.")