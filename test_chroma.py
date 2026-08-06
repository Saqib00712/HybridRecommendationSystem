from app.services.chroma_service import init_chroma, add_product_embedding, get_collection_count
from app.utils.mesh_api import generate_simple_embedding

print("Initializing ChromaDB...")
init_chroma()

print("Adding test embedding...")
text = 'Python for Beginners'
embedding = generate_simple_embedding(text)
add_product_embedding('1', text, embedding, {'title': text, 'category': 'Python'})

print(f'Collection count: {get_collection_count()}')
print('✅ ChromaDB working!')