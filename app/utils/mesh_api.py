"""
Mesh API + Free Embeddings Integration
LLM calls go through Mesh API. Embeddings use free sentence-transformers.
"""
import hashlib
from typing import List
from openai import OpenAI
from app.config import get_settings

settings = get_settings()

# Mesh client for LLM calls only
client = None
if settings.mesh_api_key and settings.mesh_api_key != "your-mesh-api-key-here":
    client = OpenAI(
        base_url="https://api.meshapi.ai/v1",
        api_key=settings.mesh_api_key
    )
    print(f"✅ Mesh API client initialized (model: {settings.mesh_model})")
else:
    print("⚠️ Mesh API key not set")

# Free embedding model (load once)
embedding_model = None

def get_embedding_model():
    """Load free sentence-transformer model"""
    global embedding_model
    if embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("🔄 Loading free embedding model (all-MiniLM-L6-v2)...")
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Free embedding model loaded (384 dimensions)")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
    return embedding_model


def generate_simple_embedding(text: str, dimensions: int = 384) -> List[float]:
    """Fallback: Hash-based embedding"""
    hash_bytes = hashlib.sha256(text.encode()).digest()
    return [((hash_bytes[i % len(hash_bytes)] / 255.0) * 2 - 1) for i in range(dimensions)]


async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding using FREE sentence-transformers.
    Falls back to hash if model not available.
    """
    model = get_embedding_model()
    if model:
        try:
            embedding = model.encode(text).tolist()
            return embedding
        except Exception as e:
            print(f"Embedding failed: {e}")
    
    return generate_simple_embedding(text)


def extract_content_from_response(response) -> str:
    """Extract content from Mesh API response"""
    if not response.choices or len(response.choices) == 0:
        return ""
    
    msg = response.choices[0].message
    content = msg.content
    
    if content and content.strip():
        return content.strip()
    
    if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
        text = msg.reasoning_content
        if "Draft" in text:
            parts = text.split("Draft")
            if len(parts) > 1:
                content = parts[-1].split(":")[-1].strip()
                sentences = content.replace('!', '.').replace('?', '.').split('.')
                return '. '.join(s[:100] for s in sentences[:3] if s.strip()).strip()
    
    return ""


async def generate_recommendation_message(user_interests: str, product_list: list) -> str:
    """Generate personalized recommendation using Mesh API LLM"""
    if client:
        try:
            product_descriptions = "\n".join([
                f"- {p['title']} ({p['category']}, {p['difficulty']})"
                for p in product_list[:5]
            ])
            
            prompt = f"""Write a short personalized course recommendation (2-3 sentences).

User interests: {user_interests}

Courses: {product_descriptions}

Be persuasive and encouraging."""

            response = client.chat.completions.create(
                model=settings.mesh_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            content = extract_content_from_response(response)
            if content:
                return content
                
        except Exception as e:
            print(f"Mesh LLM error: {e}")
    
    # Fallback
    product_names = [p["title"] for p in product_list[:3]]
    return f"Based on your interest in {user_interests}, we recommend: {', '.join(product_names)}. Start learning today!"