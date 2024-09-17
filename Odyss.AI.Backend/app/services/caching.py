from aiocache import caches, cached
from aiocache.serializers import JsonSerializer

# Konfiguration des Caches
caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': "127.0.0.1",
        'port': 6379,
        'timeout': 1,
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        }
    }
})

class CachingService:
    def __init__(self):
        self.cache = caches.get('default')

    async def set(self, key, value, ttl=600):
        """Fügt einen neuen Wert in den Cache ein."""
        await self.cache.set(key, value, ttl=ttl)

    async def get(self, key):
        """Überprüft, ob ein Wert im Cache enthalten ist und gibt ihn zurück."""
        return await self.cache.get(key)

    async def exists(self, key):
        """Überprüft, ob ein Schlüssel im Cache existiert."""
        return await self.cache.exists(key)

    async def delete(self, key):
        """Löscht einen Wert aus dem Cache."""
        await self.cache.delete(key)

    async def update(self, key, value, ttl=600):
        """Aktualisiert einen Wert im Cache."""
        await self.cache.set(key, value, ttl=ttl)

    async def clear(self):
        """Löscht alle Werte aus dem Cache."""
        await self.cache.clear()