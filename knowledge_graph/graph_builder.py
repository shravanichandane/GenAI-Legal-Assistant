import os
from neo4j import GraphDatabase

class LegalGraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def build_graph(self, documents, clauses):
        with self.driver.session() as session:
            for doc in documents:
                session.execute_write(self._create_document_node, doc)
            for clause in clauses:
                session.execute_write(self._create_clause_node, clause)
                session.execute_write(self._create_relationship, clause)

    @staticmethod
    def _create_document_node(tx, doc):
        query = (
            "MERGE (d:Document {doc_id: $doc_id}) "
            "SET d.title = $title, d.date = $date"
        )
        tx.run(query, doc_id=doc['id'], title=doc['title'], date=doc.get('date', ''))

    @staticmethod
    def _create_clause_node(tx, clause):
        query = (
            "MERGE (c:Clause {clause_id: $clause_id}) "
            "SET c.text = $text, c.type = $type, c.risk_level = $risk"
        )
        tx.run(query, clause_id=clause['id'], text=clause['text'], type=clause['type'], risk=clause['risk_level'])

    @staticmethod
    def _create_relationship(tx, clause):
        query = (
            "MATCH (d:Document {doc_id: $doc_id}) "
            "MATCH (c:Clause {clause_id: $clause_id}) "
            "MERGE (d)-[:CONTAINS]->(c)"
        )
        tx.run(query, doc_id=clause['document_id'], clause_id=clause['id'])

if __name__ == "__main__":
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    builder = LegalGraphBuilder(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    docs = [{"id": 1, "title": "NDA_Agreement.pdf", "date": "2023-01-01"}]
    clauses = [{
        "id": 101, 
        "document_id": 1, 
        "text": "Confidential information shall not be disclosed.", 
        "type": "CONFIDENTIALITY", 
        "risk_level": "LOW"
    }]
    
    builder.build_graph(docs, clauses)
    builder.close()
    print("Graph built successfully.")
