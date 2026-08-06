"""
ChromaDB Service for vector storage and retrieval
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional
from app.config import get_settings

settings = get_settings()

# Global ChromaDB client and collection
chroma_client = None
product_collection = None


def init_chroma():
    """Initialize ChromaDB client and collection"""
    global chroma_client, product_collection
    
    try:
        chroma_client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        product_collection = chroma_client.get_or_create_collection(
            name="products",
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"✅ ChromaDB initialized with {product_collection.count()} documents")
        
    except Exception as e:
        print(f"⚠️ ChromaDB error: {e}, using in-memory fallback")
        chroma_client = chromadb.Client(ChromaSettings(anonymized_telemetry=False))
        product_collection = chroma_client.get_or_create_collection(
            name="products",
            metadata={"hnsw:space": "cosine"}
        )


def add_product_embedding(product_id: str, text: str, embedding: List[float], metadata: dict):
    """Add product embedding to ChromaDB"""
    if product_collection:
        try:
            product_collection.add(
                ids=[str(product_id)],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            print(f"Error adding to ChromaDB: {e}")
            return False
    return False


def update_product_embedding(product_id: str, text: str, embedding: List[float], metadata: dict):
    """Update product embedding in ChromaDB"""
    if product_collection:
        try:
            product_collection.update(
                ids=[str(product_id)],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            print(f"Error updating ChromaDB: {e}")
            return False
    return False


def delete_product_embedding(product_id: str):
    """Delete product embedding from ChromaDB"""
    if product_collection:
        try:
            product_collection.delete(ids=[str(product_id)])
            return True
        except Exception as e:
            print(f"Error deleting from ChromaDB: {e}")
            return False
    return False


def search_similar_products(query_embedding: List[float], n_results: int = 5) -> dict:
    """Search for similar products in ChromaDB"""
    if product_collection and product_collection.count() > 0:
        results = product_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
    return {"ids": [[]], "distances": [[]], "metadatas": [[]], "documents": [[]]}


def get_collection_count() -> int:
    """Get number of documents in collection"""
    if product_collection:
        return product_collection.count()
    return 0