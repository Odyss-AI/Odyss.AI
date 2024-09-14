import uuid
import aiohttp
import asyncio

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchAny
from app.models.user import Document
from app.config import Config

class SimailaritySearchService:
    def __init__(self):
        self.tei_url = Config.TEI_URL + "/embed"
        self.qdrant_client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
        self.collection_name = 'doc_embeddings'
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={'size': 1024, 'distance': 'Cosine'}
        )

    async def save_embedding_async(self, doc_id: str, embeddings: list):
        try:
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding[0],
                    payload={
                        "doc_id": doc_id,
                        "chunk_id": embedding[1]
                        }
                )
                for embedding in embeddings
            ]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Embeddings für Dokument {doc_id} erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Embeddings: {e}")

    async def fetch_embedding_async(self, to_embed: str, chunk_id: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                    if response.status == 200:
                        response_json = await response.json()  # Stelle sicher, dass await verwendet wird
                        if isinstance(response_json, list) and len(response_json) > 0 and isinstance(response_json[0], list):
                            return [response_json[0], chunk_id]  # Rückgabe des ersten Elements der Liste
                        else:
                            print("Fehler: Unerwartetes Format der API-Antwort.")
                            return None
                    else:
                        print(f"Fehler: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"HTTP-Fehler: {e}")
            return None

    async def create_embeddings_async(self, doc: Document):
        tasks = []
        for chunk in doc.textList:
            tasks.append(self.fetch_embedding_async(chunk.text, chunk.id))
        for img in doc.imgList:
            tasks.append(self.fetch_embedding_async(img.imgtext, img.id))
            tasks.append(self.fetch_embedding_async(img.llm_output, img.id))
        
        embeddings = await asyncio.gather(*tasks)
        
        return embeddings

    async def search_similar_documents(self, doc_ids: list, query: str, count: int = 5):
        try:
            # Fetch embeddings for the query
            query_embeddings = await self.fetch_embedding_async(query, "q")
            
            # Verwende MatchAny, um eine Liste von Werten zu filtern
            filter = Filter(
                must=[
                    FieldCondition(
                        key="doc_id",  # Das Feld, das gefiltert werden soll
                        match=MatchAny(any=doc_ids)  # Verwende MatchAny anstelle von MatchValue
                    )
                ]
            )

            # Search for similar documents with the filter
            results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embeddings[0],
                limit=count,
                query_filter=filter  # Korrigierte Filter-Übergabe
            )
            
            # Extract chunk_ids from the payload of the top results
            chunk_ids = [result.payload['chunk_id'] for result in results]
            
            return chunk_ids
        except Exception as e:
            print(f"Fehler bei der Dokumentsuche: {e}")
            return None

