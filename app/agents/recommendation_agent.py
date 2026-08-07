
"""
Recommendation Agent - LangGraph-style Workflow with Hybrid Search
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import asyncio
import time

from app.models.product import Product
from app.models.behavior import UserBehavior
from app.services.chroma_service import search_similar_products
from app.utils.mesh_api import generate_embedding
from app.utils.langsmith_config import trace_agent_step, trace_recommendation


@trace_agent_step("load_activity")
def load_user_activity(user_id: int, db: Session) -> List[Dict]:
    behaviors = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id
    ).order_by(UserBehavior.timestamp.desc()).limit(20).all()
    
    return [{
        "event_type": b.event_type, "product_id": b.product_id,
        "search_query": b.search_query, "category": b.category,
        "time_spent": b.time_spent
    } for b in behaviors]


@trace_agent_step("analyze_interests")
def analyze_interests(activities: List[Dict], db: Session) -> Dict[str, Any]:
    categories, tags, total_time = {}, {}, {}
    last_viewed = None
    
    for a in activities:
        if a["event_type"] == "product_view" and a["product_id"]:
            product = db.query(Product).filter(Product.id == a["product_id"]).first()
            if product:
                categories[product.category] = categories.get(product.category, 0) + 1
                for tag in product.tags.split(","):
                    tags[tag.strip()] = tags.get(tag.strip(), 0) + 1
                if a.get("time_spent"):
                    total_time[product.category] = total_time.get(product.category, 0) + a["time_spent"]
                if last_viewed is None:
                    last_viewed = product.category
        if a["event_type"] == "search" and a["search_query"]:
            tags[a["search_query"]] = tags.get(a["search_query"], 0) + 1
    
    return {"categories": categories, "tags": tags, "last_viewed_category": last_viewed, "total_time": total_time}


def rerank(products: List[Dict], interests: Dict) -> List[Dict]:
    if not products: return products
    cats = interests.get("categories", {})
    tags = interests.get("tags", {})
    last_cat = interests.get("last_viewed_category", "")
    total_time = interests.get("total_time", {})
    
    def score(p):
        s = 0
        if p["category"] == last_cat: s += 15
        if p["category"] in cats: s += cats[p["category"]] * 3
        if p["category"] in total_time: s += total_time[p["category"]] * 0.1
        for t in p.get("tags","").split(","):
            if t.strip() in tags: s += tags[t.strip()]
        if p["difficulty"] in ["Beginner","Intermediate"]: s += 1
        return s
    
    return sorted(products, key=score, reverse=True)


@trace_agent_step("retrieve_products")
def retrieve_similar_products(interests: Dict[str, Any], db: Session) -> List[Dict]:
    retrieved, seen_ids = [], set()
    categories = interests.get("categories", {})
    last_category = interests.get("last_viewed_category")
    tags = interests.get("tags", {})
    total_time = interests.get("total_time", {})
    
    sorted_cats = sorted(categories.items(), key=lambda x: total_time.get(x[0], 0), reverse=True)
    top_categories = [c[0] for c in sorted_cats[:3]]
    
    # Same category
    if last_category:
        for p in db.query(Product).filter(Product.category == last_category).order_by(func.random()).limit(3).all():
            if p.id not in seen_ids:
                retrieved.append(product_to_dict(p)); seen_ids.add(p.id)
    
    # Top categories
    for cat in top_categories:
        if cat != last_category and len(retrieved) < 5:
            for p in db.query(Product).filter(Product.category == cat).order_by(func.random()).limit(2).all():
                if p.id not in seen_ids and len(retrieved) < 5:
                    retrieved.append(product_to_dict(p)); seen_ids.add(p.id)
    
    # ChromaDB
    if len(retrieved) < 5 and top_categories:
        query_text = " ".join(top_categories + list(tags.keys())[:5])
        try:
            loop = asyncio.new_event_loop()
            emb = loop.run_until_complete(generate_embedding(query_text))
            loop.close()
            results = search_similar_products(emb, n_results=5)
            if results["ids"] and results["ids"][0]:
                for pid in results["ids"][0]:
                    if len(retrieved) >= 5: break
                    p = db.query(Product).filter(Product.id == int(pid)).first()
                    if p and p.id not in seen_ids:
                        retrieved.append(product_to_dict(p)); seen_ids.add(p.id)
        except Exception as e: print(f"ChromaDB: {e}")
    
    # HYBRID: Keyword search
    if len(retrieved) < 5 and top_categories:
        for cat in top_categories[:2]:
            for p in db.query(Product).filter(
                (Product.title.ilike(f'%{cat}%')) | (Product.description.ilike(f'%{cat}%')) | (Product.tags.ilike(f'%{cat}%'))
            ).limit(3).all():
                if p.id not in seen_ids and len(retrieved) < 5:
                    retrieved.append(product_to_dict(p)); seen_ids.add(p.id)
    
    # Fill
    if len(retrieved) < 3:
        for p in db.query(Product).order_by(func.random()).limit(5).all():
            if p.id not in seen_ids and len(retrieved) < 5:
                retrieved.append(product_to_dict(p)); seen_ids.add(p.id)
    
    return rerank(retrieved, interests)[:5]


def product_to_dict(p: Product) -> Dict:
    return {"id": p.id, "title": p.title, "category": p.category, "description": p.description[:100],
            "difficulty": p.difficulty, "price": p.price, "instructor": p.instructor,
            "duration": p.duration, "tags": p.tags}


@trace_agent_step("generate_message")
def generate_message(interests: Dict[str, Any], products: List[Dict]) -> str:
    if not products: return "Browse more courses to get personalized recommendations!"
    cats = interests.get("categories", {})
    interest_str = ", ".join(list(cats.keys())[:3]) or "technology"
    
    try:
        from app.utils.mesh_api import generate_recommendation_message as mesh_gen
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        msg = loop.run_until_complete(mesh_gen(interest_str, products))
        loop.close()
        if msg and len(msg) > 20: return msg
    except Exception as e: print(f"Mesh: {e}")
    
    names = [p["title"] for p in products[:3]]
    return f"Based on your interest in {interest_str}, we recommend: {', '.join(names)}. Start learning today!"


def run_recommendation_agent(user_id: int, db: Session) -> Dict[str, Any]:
    start = time.time()
    steps = {}
    try:
        activities = load_user_activity(user_id, db)
        steps["load"] = f"{len(activities)} activities"
        interests = analyze_interests(activities, db)
        steps["analyze"] = f"{len(interests.get('categories',{}))} categories"
        products = retrieve_similar_products(interests, db)
        steps["retrieve"] = f"{len(products)} products (hybrid)"
        message = generate_message(interests, products)
        steps["generate"] = f"{len(message)} chars"
        
        exec_time = f"{time.time() - start:.2f}s"
        result = {"success": True, "message": message, "product_ids": [p["id"] for p in products],
                  "products": products, "interests": {"categories": list(interests.get("categories",{}).keys()),
                  "last_viewed": interests.get("last_viewed_category")}, "execution_time": exec_time}
        
        trace_recommendation(user_id, steps, result)
        print(f"✅ [AGENT] {exec_time} | {len(products)} products (hybrid search)")
        return result
    except Exception as e:
        return {"success": False, "message": str(e), "product_ids": [], "products": [], "interests": {}}