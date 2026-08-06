"""
Mesh API Integration
For now uses simple hash-based embeddings as placeholder
Will be replaced with real Mesh API calls later
"""
import hashlib
from typing import List


def generate_simple_embedding(text: str, dimensions: int = 384) -> List[float]:
    """
    Generate a simple embedding from text using hash.
    This is a PLACEHOLDER until we integrate real Mesh API.
    """
    # Create hash of text
    hash_bytes = hashlib.sha256(text.encode()).digest()
    
    # Convert to list of floats
    embedding = []
    for i in range(dimensions):
        # Use different parts of hash for each dimension
        byte_val = hash_bytes[i % len(hash_bytes)]
        embedding.append((byte_val / 255.0) * 2 - 1)  # Scale to [-1, 1]
    
    return embedding


async def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text (placeholder)"""
    return generate_simple_embedding(text)


async def generate_recommendation_message(user_interests: str, products: list) -> str:
    """Generate personalized recommendation message (placeholder)"""
    return "Based on your interests, we recommend these courses to help you advance your skills."