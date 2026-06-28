from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.store = VectorStore()
        self.collection = self.store.collection

    def retrieve(self, query, top_k=3):

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return results