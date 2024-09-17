import uuid
import aiohttp
import asyncio

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchAny, VectorParams, HnswConfigDiff, OptimizersConfigDiff 
from app.models.user import Document
from app.config import Config

class SimailaritySearchService:
    def __init__(self):
        self.tei_url = Config.TEI_URL + "/embed"
        self.qdrant_client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
        self.collection_name = 'doc_embeddings'
        self._initialize_collection()

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
    
    async def save_embedding_async(self, id, embeddings):
        try:
            points = []
            for embedding in embeddings:
                points.append(PointStruct(id=str(uuid.uuid4()), vector=embedding[0], payload={"doc_id": id, "chunk_id": embedding[1]}))

            result = self.qdrant_client.upsert(
                collection_name=self.collection_name, 
                wait=True, 
                points=points
                )
            
            return result.status == 'completed'
            
        except Exception as e:
            print(f"Fehler beim Speichern des Embeddings: {e}")
            return None

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



            # # Search for similar documents with the filter
            # results = self.qdrant_client.query_points(
            #     collection_name=self.collection_name,
            #     query=query_embeddings[0],
            #     limit=count,
            #     # query_filter=filter,
            #     with_payload=True,
            #     with_vectors=False
            # )

            search_result = self.qdrant_client.query_points(
                collection_name=self.collection_name, 
                query=query_embeddings[0], 
                limit=5,
                with_payload=True,
                with_vectors=True
            ).points
                        
            # Extract chunk_ids from the payload of the top results
            chunk_ids = []
            chunk_ids = [[result.payload['chunk_id'], result.score] for result in search_result]
            
            return chunk_ids
        except Exception as e:
            print(f"Fehler bei der Dokumentsuche: {e}")
            return None

    def _initialize_collection(self):
        # Überprüfen, ob die Collection bereits existiert
        try:
            collections = self.qdrant_client.get_collections()
            col_names = []
            for collection in collections:
                if len(collection[1]) > 0:
                    col_names.append(str(collection[1][0].name))
        except Exception as e:
            print(f"Fehler beim Abrufen der Collections: {e}")
            return
        
        if self.collection_name not in col_names:

            # Erstelle die Collection
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1024, distance='Cosine'),
                on_disk_payload=True,
                hnsw_config=HnswConfigDiff(
                    m=16,
                    ef_construct=100,
                    full_scan_threshold=10000,
                    max_indexing_threads=0,
                    on_disk=True
                ),
                optimizers_config=OptimizersConfigDiff(
                    deleted_threshold=0.0,
                    vacuum_min_vector_number=0,
                    indexing_threshold=10000,
                    flush_interval_sec=5
                )
            )
            print(f"Collection '{self.collection_name}' erstellt.")
        else:
            print(f"Collection '{self.collection_name}' existiert bereits.")