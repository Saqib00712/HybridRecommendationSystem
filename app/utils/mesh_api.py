"""
Mesh API Integration - MANDATORY for SmartReco Challenge
All LLM/AI calls go through Mesh API
"""
import hashlib
from typing import List
from openai import OpenAI
from app.config import get_settings

settings = get_settings()

# Initialize Mesh client (OpenAI-compatible)
client = None
if settings.mesh_api_key and settings.mesh_api_key != "your-mesh-api-key-here":
    client = OpenAI(
        base_url="https://api.meshapi.ai/v1",
        api_key=settings.mesh_api_key
    )
    print(f"✅ Mesh API client initialized (model: {settings.mesh_model})")
else:
    print("⚠️ Mesh API key not set - using fallback")


def generate_simple_embedding(text: str, dimensions: int = 384) -> List[float]:
    """Fallback embedding from hash"""
    hash_bytes = hashlib.sha256(text.encode()).digest()
    return [((hash_bytes[i % len(hash_bytes)] / 255.0) * 2 - 1) for i in range(dimensions)]


async def generate_embedding(text: str) -> List[float]:
    """Generate embedding using Mesh API"""
    if client:
        try:
            response = client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Mesh embedding failed: {e}")
    return generate_simple_embedding(text)


def extract_content_from_response(response) -> str:
    """
    Extract content from Mesh API response.
    Handles different model response formats.
    """
    if not response.choices or len(response.choices) == 0:
        return ""
    
    msg = response.choices[0].message
    
    # Try regular content first
    content = msg.content
    if content and content.strip():
        return content.strip()
    
    # Try reasoning_content (some models put response here)
    if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
        text = msg.reasoning_content
        
        # Extract final recommendation from reasoning
        # Look for the last complete sentence after "Draft"
        if "Draft 1:" in text or "Draft:" in text:
            drafts = text.split("Draft")
            # Take the last draft
            last_draft = drafts[-1]
            # Get content after colon
            if ":" in last_draft:
                content = last_draft.split(":", 1)[-1].strip()
                # Take first 2-3 sentences
                sentences = content.replace('!', '.').replace('?', '.').split('.')
                return '. '.join(s[:100] for s in sentences[:3] if s.strip()).strip()
        
        # If no draft format, take the last meaningful part
        sentences = text.split('.')
        relevant = [s for s in sentences if any(word in s.lower() for word in 
            ['recommend', 'course', 'start', 'learn', 'skill', 'build', 'perfect', 'begin'])]
        if relevant:
            return '. '.join(relevant[-2:]).strip()
    
    return ""


async def generate_recommendation_message(
    user_interests: str,
    product_list: list
) -> str:
    """Generate personalized recommendation using Mesh API LLM"""
    if client:
        try:
            product_descriptions = "\n".join([
                f"- {p['title']} ({p['category']}, {p['difficulty']})"
                for p in product_list[:5]
            ])
            
            prompt = f"""Write a short personalized course recommendation (2-3 sentences).

User is interested in: {user_interests}

Courses to recommend:
{product_descriptions}

Be persuasive and encouraging. End with a call to action."""

            response = client.chat.completions.create(
                model=settings.mesh_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Extract content from response
            content = extract_content_from_response(response)
            
            if content:
                print(f"✅ Mesh LLM generated: {content[:80]}...")
                return content
            else:
                print("⚠️ Empty response from Mesh API, using fallback")
                
        except Exception as e:
            print(f"Mesh LLM error: {e}, using fallback")
    
    # Fallback message
    product_names = [p["title"] for p in product_list[:3]]
    if product_names:
        return (
            f"Based on your interest in {user_interests}, we recommend starting with "
            f"{product_names[0]}. This course perfectly matches your learning journey "
            f"and will help you build practical skills. Start learning today!"
        )
    return "Explore our courses to find the perfect match for your interests!"


async def generate_rag_response(query: str, context: str) -> str:
    """
    Generate RAG response using Mesh API.
    Used for more complex recommendation queries.
    """
    if client:
        try:
            prompt = f"""Based on the following information, answer the query.

Context: {context}

Query: {query}

Provide a helpful, concise response."""

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
            print(f"Mesh RAG error: {e}")
    
    return "Based on your interests, we have several courses that match your needs."