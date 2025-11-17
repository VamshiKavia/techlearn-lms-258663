from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.core.config import get_settings

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    """Initialize the MongoDB client and database."""
    global _client, _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.MONGO_URI)
    _db = _client[settings.MONGO_DB_NAME]


async def close_mongo_connection() -> None:
    """Close MongoDB client connection."""
    global _client, _db
    if _client:
        _client.close()
    _client = None
    _db = None


def get_db() -> AsyncIOMotorDatabase:
    """Get the active Mongo database instance.

    Raises:
        RuntimeError: If the database is not initialized.

    Returns:
        AsyncIOMotorDatabase: database instance.
    """
    if _db is None:
        raise RuntimeError("Database not initialized. Ensure startup event ran.")
    return _db


def get_collection(name: str) -> AsyncIOMotorCollection:
    """Get a collection by name.

    Args:
        name: collection name.

    Returns:
        AsyncIOMotorCollection: collection handle.
    """
    return get_db()[name]
