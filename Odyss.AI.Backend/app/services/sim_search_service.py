import uuid
import aiohttp
import asyncio
import logging

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchAny, VectorParams, HnswConfigDiff, OptimizersConfigDiff 
from app.models.user import Document
from app.config import config

class SimailaritySearchService:
    """
    A service for performing similarity search operations using Qdrant and TEI embeddings.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SimailaritySearchService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Verhindert mehrfache Initialisierung
            self.tei_url = config.tei_url + "/embed"
            self.qdrant_client = QdrantClient(host=config.qdrant_host, port=config.qdrant_port)
            self.collection_name = 'doc_embeddings'
            self._initialize_collection()
            self._initialized = True

    async def fetch_embedding_async(self, to_embed: str, chunk_id: str):
        """
        Fetches the embedding for a given text asynchronously.

        Args:
            to_embed (str): The text to be embedded.
            chunk_id (str): The ID of the chunk.

        Returns:
            list: A list containing the embedding and the chunk ID, or None if an error occurs.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                    if response.status == 200:
                        response_json = await response.json()  # Stelle sicher, dass await verwendet wird
                        if isinstance(response_json, list) and len(response_json) > 0 and isinstance(response_json[0], list):
                            return [response_json[0], chunk_id]  # Rückgabe des ersten Elements der Liste
                        else:
                            logging.error(f"Error fetching embedding at {chunk_id}: Invalid response")
                            return None
                    else:
                        print(f"Error at {chunk_id}: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            logging.error(f"HTTP-Error at {chunk_id}: {e}")
            return None

    async def create_embeddings_async(self, doc: Document):
        """
        Creates embeddings for the text and image chunks in a document asynchronously.

        Args:
            doc (Document): The document containing text and image chunks.

        Returns:
            list: A list of embeddings.
        """
        tasks = []
        for chunk in doc.textList:
            tasks.append(self.fetch_embedding_async(chunk.text, chunk.id))
        for img in doc.imgList:
            if(img.imgtext):
                tasks.append(self.fetch_embedding_async(img.imgtext, img.id))
            if(img.llm_output):
                tasks.append(self.fetch_embedding_async(img.llm_output, img.id))
        
        embeddings = await asyncio.gather(*tasks)
        
        return embeddings
    
    async def save_embedding_async(self, id, embeddings):
        """
        Saves the embeddings to the Qdrant collection asynchronously.

        Args:
            id (str): The document ID.
            embeddings (list): The list of embeddings to be saved.

        Returns:
            bool: True if the embeddings were successfully saved, False otherwise.
        """
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
            logging.error(f"Error while saving embeddings at document {id}: {e}")
            return None

    async def search_similar_documents_async(self, doc_ids: list, query: str, count: int = 5):
        """
        Searches for similar documents based on the provided query and document IDs asynchronously.

        Args:
            doc_ids (list): The list of document IDs to filter the search.
            query (str): The query text to search for similar documents.
            count (int, optional): The number of similar documents to return. Defaults to 5.

        Returns:
            list: A list of chunk IDs and their scores, or None if an error occurs.
        """
        try:
            # Fetch embeddings for the query
            query_embeddings = await self.fetch_embedding_async(query, "q")
            
            filter = Filter(
                must=[
                    FieldCondition(
                        # Field to filter on
                        key="doc_id",
                        # Match any of the values in the list
                        match=MatchAny(any=doc_ids)
                    )
                ]
            )

            search_result = self.qdrant_client.query_points(
                collection_name=self.collection_name, 
                query=query_embeddings[0], 
                limit=5,
                query_filter=filter,
                with_payload=True,
                with_vectors=True
            ).points
                        
            # Extract chunk_ids from the payload of the top results
            chunk_ids = []
            chunk_ids = [[result.payload['chunk_id'], result.score] for result in search_result]
            
            return chunk_ids
        except Exception as e:
            logging.error(f"Error while searching similar docs: {e}")
            return None

    def _initialize_collection(self):
        """
        Initializes the Qdrant collection if it does not already exist.
        """
        try:
            collections = self.qdrant_client.get_collections()
            col_names = []
            for collection in collections:
                if len(collection[1]) > 0:
                    col_names.append(str(collection[1][0].name))
        except Exception as e:
            logging.error(f"Error while getting collections: {e}")
            return
        
        if self.collection_name not in col_names:

            # Create the Collection
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
            logging.info(f"Collection '{self.collection_name}' created.")
        else:
            logging.info(f"Access to vector collection '{self.collection_name}'.")