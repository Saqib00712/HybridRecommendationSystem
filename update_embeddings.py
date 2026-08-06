from app.database import SessionLocal
from app.models.product import Product
from app.services.chroma_service import init_chroma, delete_product_embedding, add_product_embedding
from app.utils.mesh_api import generate_embedding
import asyncio

init_chroma()
db = SessionLocal()

products = db.query(Product).all()
print(f'Updating {len(products)} products with real embeddings...')

for i, product in enumerate(products):
    text = f'{product.title} {product.description} {product.category} {product.tags}'
    loop = asyncio.new_event_loop()
    embedding = loop.run_until_complete(generate_embedding(text))
    loop.close()
    
    # Delete old, add new
    delete_product_embedding(str(product.id))
    add_product_embedding(
        product_id=str(product.id),
        text=text,
        embedding=embedding,
        metadata={
            'title': product.title,
            'category': product.category,
            'difficulty': product.difficulty,
            'product_id': product.id
        }
    )
    
    print(f'✅ [{i+1}/50] {product.title} ({len(embedding)} dims)')

db.close()
print('✅ All products updated with real embeddings!')