class FraudRules:


    @staticmethod
    def get_undisclosed_related_party_query():

        return """
        MATCH (emp:Person)-[:OWNS|DIRECTOR_OF]->(vendor:Company)
        MATCH (main_co:Company)-[pay:TRANSFERRED_MONEY]->(vendor)
        RETURN 
            emp.id as Internal_Person, 
            vendor.id as Suspicious_Vendor, 
            pay.amount as Amount, 
            pay.date as Date
        """

    @staticmethod
    def get_circular_flow_query():

        return """
        MATCH path = (a:Company)-[:TRANSFERRED_MONEY]->(b:Company)-[:TRANSFERRED_MONEY]->(c:Company)-[:TRANSFERRED_MONEY]->(a)
        RETURN nodes(path) as Cycle
        """

    @staticmethod
    def get_high_value_unknown_vendor_query(threshold=1000000):

        return f"""
        MATCH (c:Company)-[r:TRANSFERRED_MONEY]->(v:Company)
        WHERE r.amount > {threshold}
        AND NOT (c)-[:SIGNED_CONTRACT_WITH]->(v)
        RETURN v.id as Vendor, r.amount as Unverified_Amount
        """