"""
Recommendation Agent - Smart Matching with Mesh API
Workflow: Load Activity → Analyze → Smart Retrieve → Generate (Mesh API)
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import asyncio

from app.models.product import Product
from app.models.behavior import UserBehavior
from app.services.chroma_service import search_similar_products
from app.utils.mesh_api import generate_simple_embedding


def load_user_activity(user_id: int, db: Session) -> List[Dict]:
    """Step 1: Load user's recent activity"""
    behaviors = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id
    ).order_by(UserBehavior.timestamp.desc()).limit(20).all()
    
    activities = []
    for b in behaviors:
        activities.append({
            "event_type": b.event_type,
            "product_id": b.product_id,
            "search_query": b.search_query,
            "category": b.category
        })
    
    return activities


def analyze_interests(activities: List[Dict], db: Session) -> Dict[str, Any]:
    """Step 2: Analyze user interests"""
    categories = {}
    tags = {}
    last_viewed_category = None
    
    for activity in activities:
        if activity["event_type"] == "product_view" and activity["product_id"]:
            product = db.query(Product).filter(Product.id == activity["product_id"]).first()
            if product:
                categories[product.category] = categories.get(product.category, 0) + 1
                for tag in product.tags.split(","):
                    tag = tag.strip()
                    tags[tag] = tags.get(tag, 0) + 1
                if last_viewed_category is None:
                    last_viewed_category = product.category
        
        if activity["event_type"] == "search" and activity["search_query"]:
            tags[activity["search_query"]] = tags.get(activity["search_query"], 0) + 1
    
    return {
        "categories": categories,
        "tags": tags,
        "last_viewed_category": last_viewed_category
    }


def retrieve_similar_products(interests: Dict[str, Any], db: Session) -> List[Dict]:
    """Step 3: Smart retrieval"""
    retrieved = []
    seen_ids = set()
    
    categories = interests.get("categories", {})
    last_category = interests.get("last_viewed_category")
    tags = interests.get("tags", {})
    
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    top_categories = [c[0] for c in sorted_categories[:3]]
    
    # STEP 1: Same category as last viewed
    if last_category:
        same_category = db.query(Product).filter(
            Product.category == last_category
        ).order_by(func.random()).limit(3).all()
        
        for p in same_category:
            if p.id not in seen_ids:
                retrieved.append(product_to_dict(p))
                seen_ids.add(p.id)
    
    # STEP 2: Top categories
    for cat in top_categories:
        if cat != last_category and len(retrieved) < 5:
            cat_products = db.query(Product).filter(
                Product.category == cat
            ).order_by(func.random()).limit(2).all()
            
            for p in cat_products:
                if p.id not in seen_ids and len(retrieved) < 5:
                    retrieved.append(product_to_dict(p))
                    seen_ids.add(p.id)
    
    # STEP 3: ChromaDB similarity
    if len(retrieved) < 3 and top_categories:
        query_text = " ".join(top_categories + list(tags.keys())[:5])
        try:
            query_embedding = generate_simple_embedding(query_text)
            results = search_similar_products(query_embedding, n_results=5)
            
            if results["ids"] and results["ids"][0]:
                for pid in results["ids"][0]:
                    if len(retrieved) >= 5:
                        break
                    product = db.query(Product).filter(Product.id == int(pid)).first()
                    if product and product.id not in seen_ids:
                        retrieved.append(product_to_dict(product))
                        seen_ids.add(product.id)
        except Exception as e:
            print(f"ChromaDB fallback failed: {e}")
    
    # STEP 4: Fill remaining
    if len(retrieved) < 3:
        fill_products = db.query(Product).order_by(func.random()).limit(5).all()
        for p in fill_products:
            if p.id not in seen_ids and len(retrieved) < 5:
                retrieved.append(product_to_dict(p))
                seen_ids.add(p.id)
    
    return retrieved[:5]


def product_to_dict(product: Product) -> Dict:
    """Convert product to dictionary"""
    return {
        "id": product.id,
        "title": product.title,
        "category": product.category,
        "description": product.description[:100],
        "difficulty": product.difficulty,
        "price": product.price,
        "instructor": product.instructor,
        "duration": product.duration,
        "tags": product.tags
    }


def generate_message(interests: Dict[str, Any], products: List[Dict]) -> str:
    """Step 4: Generate message using Mesh API with fallback"""
    if not products:
        return "Browse more courses to get personalized recommendations!"
    
    categories = interests.get("categories", {})
    interest_str = ", ".join(list(categories.keys())[:3]) if categories else "technology"
    
    # Try Mesh API
    try:
        from app.utils.mesh_api import generate_recommendation_message as mesh_generate
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        message = loop.run_until_complete(mesh_generate(interest_str, products))
        loop.close()
        
        if message and len(message) > 20:
            return message
    except Exception as e:
        print(f"Mesh API failed: {e}")
    
    # Fallback
    product_names = [p["title"] for p in products[:3]]
    return f"Based on your interest in {interest_str}, we recommend: {', '.join(product_names)}. Start learning today!"


def run_recommendation_agent(user_id: int, db: Session) -> Dict[str, Any]:
    """Run the complete recommendation workflow"""
    try:
        activities = load_user_activity(user_id, db)
        interests = analyze_interests(activities, db)
        products = retrieve_similar_products(interests, db)
        message = generate_message(interests, products)
        
        return {
            "success": True,
            "message": message,
            "product_ids": [p["id"] for p in products],
            "products": products,
            "interests": {
                "categories": list(interests.get("categories", {}).keys()),
                "last_viewed": interests.get("last_viewed_category")
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "product_ids": [],
            "products": [],
            "interests": {}
        }