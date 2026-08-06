"""
LangSmith Observability - Complete Integration
"""
import os
import functools
import time
from app.config import get_settings

settings = get_settings()

langsmith_enabled = False


def setup_langsmith():
    """Configure and enable LangSmith tracing"""
    global langsmith_enabled
    
    api_key = (
        settings.langsmith_api_key or 
        os.getenv("LANGCHAIN_API_KEY") or 
        os.getenv("LANGSMITH_API_KEY") or
        ""
    )
    
    if api_key and api_key != "your-langsmith-api-key-here" and len(api_key) > 10:
        os.environ["LANGCHAIN_API_KEY"] = api_key
        os.environ["LANGCHAIN_PROJECT"] = "smartreco-ai-final"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        langsmith_enabled = True
        print(f"✅ LangSmith enabled - Project: smartreco-ai-final")
        return True
    else:
        print(f"⚠️ LangSmith disabled - API key not found or invalid")
        return False


def trace_agent_step(step_name: str):
    """Decorator to trace each agent step with timing"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                print(f"📊 {step_name} → ✅ {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                print(f"❌ {step_name} → FAILED after {duration:.2f}s: {e}")
                raise
        return wrapper
    return decorator


def trace_recommendation(user_id: int, steps: dict, result: dict):
    """Send recommendation trace to LangSmith"""
    if not langsmith_enabled:
        return
    
    try:
        from langsmith import Client
        
        client = Client()
        
        run = client.create_run(
            name="Recommendation Agent",
            run_type="chain",
            inputs={"user_id": user_id},
            outputs={
                "message_preview": result.get("message", "")[:150],
                "products_count": len(result.get("products", [])),
                "execution_time": result.get("execution_time", "")
            },
            project_name="smartreco-ai-final",
            tags=["recommendation", "agent", "mesh-api"],
            metadata={
                "interests": result.get("interests", {}),
                "steps": steps
            }
        )
        
        if run:
            run_id = run.id if hasattr(run, 'id') else 'success'
            print(f"✅ LangSmith trace sent! Run ID: {run_id}")
        else:
            print("⚠️ LangSmith trace sent but no run ID returned")
        
    except Exception as e:
        print(f"⚠️ LangSmith trace error: {e}")


# Initialize on import
setup_langsmith()
