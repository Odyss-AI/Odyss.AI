import asyncio
import logging

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from aiocache import caches, Cache
from aiocache.serializers import JsonSerializer

caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        }
    }
})

class CachingService:
    def __init__(self):
        self.cache: Cache = caches.get('default')
        self.cache.serializer = JsonSerializer()

    async def set(self, key: str, value: BaseModel, ttl: int = 600) -> bool:
        """
        Adds a new value to the cache.

        Args:
            key (str): The key under which the value should be stored.
            value (BaseModel): The value to be stored, which must be a Pydantic model.
            ttl (int, optional): Time-to-live for the cache entry in seconds. Defaults to 600 seconds.

        Returns:
            bool: True if the value was successfully set, False otherwise.
        """
        try:
            await self.cache.set(key, value.json(), ttl=ttl)
            return True
        except Exception as e:
            logging.error(f"Error setting value for key {key}: {e}")
            return False

    async def get(self, key: str, model: BaseModel) -> Optional[BaseModel]:
        """
        Checks if a value is in the cache and returns it.

        Args:
            key (str): The key of the value to retrieve.
            model (BaseModel): The Pydantic model class to deserialize the cached value.

        Returns:
            Optional[BaseModel]: The deserialized value if found, None otherwise.
        """
        try:
            data = await asyncio.wait_for(self.cache.get(key), timeout=5.0)
            if data:
                return model.model_validate_json(data)
            return None
        except asyncio.TimeoutError:
            logging.error(f"TimeoutError: Retrieving value for key {key} took too long.")
            return None
        except asyncio.CancelledError:
            logging.error(f"CancelledError: Retrieving value for key {key} was cancelled.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    async def exists(self, key: str) -> bool:
        """
        Checks if a key exists in the cache.

        Args:
            key (str): The key to check for existence.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            return await self.cache.exists(key)
        except Exception as e:
            logging.error(f"Error checking existence of key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Deletes a value from the cache.

        Args:
            key (str): The key of the value to delete.

        Returns:
            bool: True if the value was successfully deleted, False otherwise.
        """
        try:
            await self.cache.delete(key)
            return True
        except Exception as e:
            logging.error(f"Error deleting key {key}: {e}")
            return False

    async def update(self, key: str, value: BaseModel, ttl: int = 600) -> bool:
        """
        Updates a value in the cache.

        Args:
            key (str): The key of the value to update.
            value (BaseModel): The new value to be stored, which must be a Pydantic model.
            ttl (int, optional): Time-to-live for the cache entry in seconds. Defaults to 600 seconds.

        Returns:
            bool: True if the value was successfully updated, False otherwise.
        """
        try:
            if await self.exists(key):
                return await self.set(key, value, ttl)
            else:
                logging.error(f"Key {key} does not exist in the cache.")
                return False
        except Exception as e:
            logging.error(f"Error updating key {key}: {e}")
            return False