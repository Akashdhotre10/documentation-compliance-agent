import json
import os

import chromadb

from chromadb.utils import embedding_functions


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="documentation",

            embedding_function=self.embedding_function
        )

    def build_database(self):

        with open(
            "data/processed/guidelines.json",
            encoding="utf-8"
        ) as file:

            pages = json.load(file)

        for page in pages:

            page_id = str(page["page"])

            title = page["title"]

            content = page["content"]

            document = f"""
            Title:
            {title}

            Content:
            {content}
            """

            self.collection.upsert(

                ids=[page_id],

                documents=[document],

                metadatas=[
                    {
                        "title": title
                    }
                ]
            )

        print()

        print("Database Created Successfully")

        print("Documents:", self.collection.count())