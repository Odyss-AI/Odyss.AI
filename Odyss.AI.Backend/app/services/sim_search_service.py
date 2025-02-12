import uuid
import aiohttp
import asyncio
import logging
import traceback
import tqdm

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

    async def fetch_embedding_async(self, to_embed: list, chunk_ids: list):
        """
        Fetches the embeddings for a given list of texts asynchronously.
 
        Args:
            to_embed (list): The list of texts to be embedded.
            chunk_ids (list): The list of chunk IDs.
 
        Returns:
            list: A list containing the embeddings and the chunk IDs, or None if an error occurs.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        if isinstance(response_json, list) and all(isinstance(item, list) for item in response_json):
                            return list(zip(response_json, chunk_ids))
                        else:
                            print(f"Error fetching embeddings: Invalid response")
                            logging.error(f"Error fetching embeddings: Invalid response")
                            return None
                    else:
                        print(f"Error: {response.status}")
                        logging.error(f"Error: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            logging.error(f"Client-Error: {e}")
            logging.error(f"HTTP-Error: {e}")
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
        chunks = [(chunk.text, chunk.id) for chunk in doc.textList]
        chunks += [(img.imgtext, img.id) for img in doc.imgList if img.imgtext]
        chunks += [(img.llm_output, img.id) for img in doc.imgList if img.llm_output]
        # Wörter zählen in den Texten der Liste
        #for text, chunk_id in chunks:
        #    anzahl_woerter = len(text.split())
        #    print(f"Chunk ID: {chunk_id}, Anzahl der Wörter: {anzahl_woerter}")
        #for i in tqdm(range(0, len(chunks), 32), desc="Processing embeddings"):
        for i in range(0, len(chunks), 14):
            batch = chunks[i:i + 14]
            texts, ids = zip(*batch)
            tasks.append(self.fetch_embedding_async(list(texts), list(ids)))
 
        embeddings = await asyncio.gather(*tasks)
        return [item for sublist in embeddings for item in sublist] if embeddings else None
    
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
            print("Saving process started for Qdrant")
            points = []

            #print(embeddings)

            for embedding in embeddings:
                points.append(PointStruct(id=str(uuid.uuid4()), vector=embedding[0], payload={"doc_id": id, "chunk_id": embedding[1]}))

            print("points: "+str(points))

            result = self.qdrant_client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=points
            )
            
            return result.status == 'completed'

        except ValueError as ve:
            print("ValueError while saving embeddings for document {id}: "+str(ve))
            logging.error(f"ValueError while saving embeddings for document {id}: {str(ve)}")
            logging.debug(traceback.format_exc())  # Log full stack trace for debugging
            return None

        except ConnectionError as ce:
            print("ConnectionError with Qdrant while saving embeddings for document {id}: "+str(ce))
            logging.error(f"ConnectionError with Qdrant while saving embeddings for document {id}: {str(ce)}")
            return None

        except Exception as e:
            print("Unexpected error while saving embeddings for document {id}: "+str(e))
            logging.error(f"Unexpected error while saving embeddings for document {id}: {str(e)}")
            logging.debug(traceback.format_exc())  # Log full stack trace for debugging
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
            print("Error while searching similar docs: "+str(e))
            logging.error(f"Error while searching similar docs: {str(e)}")
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
            print("Error while getting collections: "+str(e))
            logging.error(f"Error while getting collections: {str(e)}")
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
            print(f"Access to vector collection '{self.collection_name}'.")
            logging.info(f"Access to vector collection '{self.collection_name}'.")