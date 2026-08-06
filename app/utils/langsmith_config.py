"""
LangSmith Observability Integration
Traces every step of the recommendation workflow
"""
import os
import time
import functools
from app.config import get_settings

settings = get_settings()

# Track if LangSmith is enabled
langsmith_enabled = False


def setup_langsmith():
    """Configure LangSmith tracing"""
    global langsmith_enabled
    
    if settings.langsmith_api_key and settings.langsmith_api_key != "your-langsmith-api-key-here":
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project or "smartreco-ai"
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        langsmith_enabled = True
        print(f"✅ LangSmith enabled for project: {settings.langsmith_project}")
        return True
    else:
        print("⚠️ LangSmith API key not set - tracing disabled")
        return False


def trace_agent_step(step_name: str):
    """
    Decorator to trace each agent step.
    Logs: step name, execution time, success/failure
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                if langsmith_enabled:
                    print(f"📊 [TRACE] {step_name} → ✅ {duration:.2f}s")
                else:
                    print(f"📊 {step_name} → {duration:.2f}s")
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                print(f"❌ [TRACE] {step_name} → FAILED after {duration:.2f}s: {e}")
                raise
        return wrapper
    return decorator


# Auto-initialize
setup_langsmith()

