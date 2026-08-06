"""
Seed 50 realistic tech courses into the database
"""
from app.database import SessionLocal, init_db
from app.models.product import Product
from app.services.chroma_service import init_chroma, add_product_embedding
from app.utils.mesh_api import generate_simple_embedding

# 50 Realistic Tech Courses
courses = [
    # Artificial Intelligence
    {"title": "Introduction to Artificial Intelligence", "description": "Comprehensive introduction to AI concepts including search algorithms, knowledge representation, and reasoning.", "category": "Artificial Intelligence", "difficulty": "Beginner", "price": 59.99, "instructor": "Dr. Sarah Chen", "duration": "10 weeks", "tags": "AI,beginner,introduction,algorithms"},
    {"title": "Advanced AI Systems", "description": "Deep dive into advanced AI topics including neural architecture search and meta-learning.", "category": "Artificial Intelligence", "difficulty": "Advanced", "price": 89.99, "instructor": "Prof. James Wilson", "duration": "12 weeks", "tags": "AI,advanced,neural,meta-learning"},
    {"title": "AI Ethics and Responsible AI", "description": "Learn about ethical considerations in AI development including bias, fairness, and transparency.", "category": "Artificial Intelligence", "difficulty": "Intermediate", "price": 69.99, "instructor": "Dr. Maria Garcia", "duration": "6 weeks", "tags": "AI,ethics,responsible,fairness"},
    {"title": "Computer Vision Fundamentals", "description": "Master image processing, object detection, and convolutional neural networks for visual recognition.", "category": "Artificial Intelligence", "difficulty": "Intermediate", "price": 79.99, "instructor": "Dr. Alex Kumar", "duration": "8 weeks", "tags": "AI,computer-vision,CNN,image-processing"},
    {"title": "Natural Language Processing with AI", "description": "Build NLP applications using transformers, BERT, and GPT architectures.", "category": "Artificial Intelligence", "difficulty": "Advanced", "price": 94.99, "instructor": "Prof. Lisa Thompson", "duration": "10 weeks", "tags": "AI,NLP,transformers,BERT,GPT"},
    
    # Machine Learning
    {"title": "Machine Learning A-Z", "description": "Complete ML course covering regression, classification, clustering, and ensemble methods.", "category": "Machine Learning", "difficulty": "Beginner", "price": 49.99, "instructor": "Dr. Robert Kim", "duration": "12 weeks", "tags": "ML,regression,classification,clustering"},
    {"title": "Deep Learning Specialization", "description": "Master neural networks, backpropagation, and deep architectures for complex problems.", "category": "Machine Learning", "difficulty": "Advanced", "price": 99.99, "instructor": "Prof. Andrew Ng", "duration": "16 weeks", "tags": "ML,deep-learning,neural-networks,backpropagation"},
    {"title": "Reinforcement Learning in Practice", "description": "Build RL agents using Q-learning, policy gradients, and deep RL techniques.", "category": "Machine Learning", "difficulty": "Advanced", "price": 109.99, "instructor": "Dr. Michael Brown", "duration": "10 weeks", "tags": "ML,reinforcement-learning,Q-learning,agents"},
    {"title": "Feature Engineering Masterclass", "description": "Learn advanced techniques for creating, selecting, and transforming features for ML models.", "category": "Machine Learning", "difficulty": "Intermediate", "price": 74.99, "instructor": "Sarah Johnson", "duration": "6 weeks", "tags": "ML,feature-engineering,data-preparation"},
    {"title": "MLOps: Machine Learning Operations", "description": "Deploy, monitor, and maintain ML models in production environments.", "category": "Machine Learning", "difficulty": "Intermediate", "price": 84.99, "instructor": "David Park", "duration": "8 weeks", "tags": "ML,MLOps,deployment,monitoring"},
    
    # Generative AI
    {"title": "Generative AI Fundamentals", "description": "Introduction to generative models including GANs, VAEs, and diffusion models.", "category": "Generative AI", "difficulty": "Beginner", "price": 64.99, "instructor": "Dr. Emily White", "duration": "8 weeks", "tags": "generative-AI,GAN,VAE,diffusion"},
    {"title": "Building with Large Language Models", "description": "Create applications using GPT, Claude, and open-source LLMs with prompt engineering.", "category": "Generative AI", "difficulty": "Intermediate", "price": 89.99, "instructor": "Prof. Mark Davis", "duration": "6 weeks", "tags": "generative-AI,LLM,GPT,prompt-engineering"},
    {"title": "Stable Diffusion & Image Generation", "description": "Master text-to-image generation using Stable Diffusion and fine-tuning techniques.", "category": "Generative AI", "difficulty": "Intermediate", "price": 79.99, "instructor": "Anna Lee", "duration": "6 weeks", "tags": "generative-AI,stable-diffusion,image-generation"},
    {"title": "Video Generation with AI", "description": "Learn to generate and edit videos using state-of-the-art AI models.", "category": "Generative AI", "difficulty": "Advanced", "price": 99.99, "instructor": "Dr. Ryan Taylor", "duration": "8 weeks", "tags": "generative-AI,video,editing,AI-models"},
    {"title": "Music and Audio Generation", "description": "Create music and audio content using generative AI models and tools.", "category": "Generative AI", "difficulty": "Intermediate", "price": 69.99, "instructor": "Chris Martin", "duration": "5 weeks", "tags": "generative-AI,music,audio,creativity"},
    
    # Agentic AI
    {"title": "Introduction to Agentic AI", "description": "Build autonomous AI agents that can plan, reason, and execute complex tasks.", "category": "Agentic AI", "difficulty": "Beginner", "price": 74.99, "instructor": "Dr. Jessica Brown", "duration": "8 weeks", "tags": "agentic-AI,agents,autonomous,planning"},
    {"title": "Multi-Agent Systems", "description": "Design systems with multiple AI agents that collaborate and compete.", "category": "Agentic AI", "difficulty": "Advanced", "price": 109.99, "instructor": "Prof. Daniel Lee", "duration": "12 weeks", "tags": "agentic-AI,multi-agent,collaboration,competition"},
    {"title": "Building AI Copilots", "description": "Create AI assistants and copilots for various domains using agent architectures.", "category": "Agentic AI", "difficulty": "Intermediate", "price": 84.99, "instructor": "Mike Wilson", "duration": "6 weeks", "tags": "agentic-AI,copilot,assistant,architecture"},
    {"title": "Tool-Using AI Agents", "description": "Develop agents that can use APIs, databases, and external tools autonomously.", "category": "Agentic AI", "difficulty": "Intermediate", "price": 89.99, "instructor": "Dr. Sarah Kim", "duration": "7 weeks", "tags": "agentic-AI,tools,APIs,autonomous"},
    {"title": "AI Agent Safety and Alignment", "description": "Ensure AI agents behave safely and align with human values and intentions.", "category": "Agentic AI", "difficulty": "Advanced", "price": 94.99, "instructor": "Prof. Alan Chen", "duration": "8 weeks", "tags": "agentic-AI,safety,alignment,ethics"},
    
    # LangGraph
    {"title": "LangGraph Fundamentals", "description": "Build stateful AI applications with LangGraph for complex agent workflows.", "category": "LangGraph", "difficulty": "Beginner", "price": 59.99, "instructor": "LangChain Team", "duration": "4 weeks", "tags": "langgraph,stateful,agents,workflows"},
    {"title": "Advanced LangGraph Patterns", "description": "Master complex graph-based agent architectures and advanced state management.", "category": "LangGraph", "difficulty": "Advanced", "price": 89.99, "instructor": "Dr. James Liu", "duration": "6 weeks", "tags": "langgraph,advanced,patterns,state-management"},
    {"title": "LangGraph for Enterprise", "description": "Deploy production-ready LangGraph applications with monitoring and scaling.", "category": "LangGraph", "difficulty": "Intermediate", "price": 99.99, "instructor": "Enterprise AI Team", "duration": "8 weeks", "tags": "langgraph,enterprise,deployment,scaling"},
    
    # LangChain
    {"title": "LangChain Complete Guide", "description": "Master LangChain for building LLM-powered applications from scratch.", "category": "LangChain", "difficulty": "Beginner", "price": 54.99, "instructor": "LangChain Experts", "duration": "6 weeks", "tags": "langchain,LLM,applications,chains"},
    {"title": "LangChain Advanced RAG", "description": "Build sophisticated retrieval-augmented generation systems with LangChain.", "category": "LangChain", "difficulty": "Advanced", "price": 89.99, "instructor": "Dr. Rachel Wong", "duration": "8 weeks", "tags": "langchain,RAG,retrieval,generation"},
    {"title": "LangChain Agents and Tools", "description": "Create intelligent agents with tool-use capabilities using LangChain framework.", "category": "LangChain", "difficulty": "Intermediate", "price": 79.99, "instructor": "Tom Anderson", "duration": "6 weeks", "tags": "langchain,agents,tools,framework"},
    
    # Python
    {"title": "Python Programming Masterclass", "description": "Complete Python course from basics to advanced concepts including OOP and decorators.", "category": "Python", "difficulty": "Beginner", "price": 39.99, "instructor": "John Smith", "duration": "10 weeks", "tags": "python,programming,OOP,basics"},
    {"title": "Python for Data Analysis", "description": "Use Python with Pandas, NumPy, and Matplotlib for powerful data analysis.", "category": "Python", "difficulty": "Intermediate", "price": 59.99, "instructor": "Dr. Lisa Park", "duration": "6 weeks", "tags": "python,data-analysis,pandas,numpy"},
    {"title": "Advanced Python Patterns", "description": "Master design patterns, async programming, and performance optimization in Python.", "category": "Python", "difficulty": "Advanced", "price": 79.99, "instructor": "Guido van Rossum", "duration": "8 weeks", "tags": "python,advanced,patterns,async"},
    {"title": "Python Web Scraping", "description": "Build powerful web scrapers using BeautifulSoup, Scrapy, and Selenium.", "category": "Python", "difficulty": "Intermediate", "price": 49.99, "instructor": "Web Data Expert", "duration": "4 weeks", "tags": "python,web-scraping,beautifulsoup,scrapy"},
    
    # Data Science
    {"title": "Data Science Bootcamp", "description": "Intensive data science program covering statistics, visualization, and machine learning.", "category": "Data Science", "difficulty": "Beginner", "price": 69.99, "instructor": "Dr. Data Team", "duration": "12 weeks", "tags": "data-science,statistics,visualization,ML"},
    {"title": "Statistical Analysis with R", "description": "Master statistical methods and hypothesis testing using R programming.", "category": "Data Science", "difficulty": "Intermediate", "price": 64.99, "instructor": "Prof. Statistics", "duration": "8 weeks", "tags": "data-science,statistics,R,hypothesis-testing"},
    {"title": "Big Data Analytics", "description": "Process and analyze large datasets using Spark, Hadoop, and cloud platforms.", "category": "Data Science", "difficulty": "Advanced", "price": 94.99, "instructor": "Big Data Expert", "duration": "10 weeks", "tags": "data-science,big-data,spark,hadoop"},
    {"title": "Data Visualization Mastery", "description": "Create compelling visualizations with Tableau, Power BI, and D3.js.", "category": "Data Science", "difficulty": "Beginner", "price": 54.99, "instructor": "Viz Specialist", "duration": "5 weeks", "tags": "data-science,visualization,tableau,power-bi"},
    
    # FastAPI
    {"title": "FastAPI Complete Course", "description": "Build production-ready APIs with FastAPI including authentication and database integration.", "category": "FastAPI", "difficulty": "Beginner", "price": 49.99, "instructor": "Sebastian Ramirez", "duration": "6 weeks", "tags": "fastapi,API,authentication,database"},
    {"title": "FastAPI Microservices", "description": "Design and deploy microservices architecture using FastAPI and Docker.", "category": "FastAPI", "difficulty": "Advanced", "price": 84.99, "instructor": "Microservices Pro", "duration": "8 weeks", "tags": "fastapi,microservices,docker,architecture"},
    {"title": "FastAPI with GraphQL", "description": "Combine FastAPI with GraphQL for flexible and efficient API development.", "category": "FastAPI", "difficulty": "Intermediate", "price": 69.99, "instructor": "API Expert", "duration": "5 weeks", "tags": "fastapi,graphQL,API,efficient"},
    
    # Cloud
    {"title": "AWS Cloud Practitioner", "description": "Prepare for AWS certification and master cloud fundamentals.", "category": "Cloud", "difficulty": "Beginner", "price": 44.99, "instructor": "AWS Trainer", "duration": "8 weeks", "tags": "cloud,AWS,certification,fundamentals"},
    {"title": "Azure Solutions Architecture", "description": "Design and implement solutions on Microsoft Azure cloud platform.", "category": "Cloud", "difficulty": "Advanced", "price": 99.99, "instructor": "Azure Expert", "duration": "12 weeks", "tags": "cloud,azure,architecture,solutions"},
    {"title": "Google Cloud Professional", "description": "Master Google Cloud Platform services and prepare for certification.", "category": "Cloud", "difficulty": "Intermediate", "price": 79.99, "instructor": "GCP Specialist", "duration": "10 weeks", "tags": "cloud,GCP,certification,services"},
    {"title": "Multi-Cloud Strategy", "description": "Learn to design and manage applications across multiple cloud providers.", "category": "Cloud", "difficulty": "Advanced", "price": 109.99, "instructor": "Cloud Architect", "duration": "8 weeks", "tags": "cloud,multi-cloud,strategy,management"},
    
    # DevOps
    {"title": "DevOps Engineering", "description": "Master CI/CD, containerization, and infrastructure as code practices.", "category": "DevOps", "difficulty": "Beginner", "price": 59.99, "instructor": "DevOps Expert", "duration": "10 weeks", "tags": "devops,CI/CD,containers,IaC"},
    {"title": "Kubernetes in Production", "description": "Deploy and manage containerized applications with Kubernetes at scale.", "category": "DevOps", "difficulty": "Advanced", "price": 94.99, "instructor": "K8s Specialist", "duration": "8 weeks", "tags": "devops,kubernetes,containers,orchestration"},
    {"title": "Terraform Infrastructure", "description": "Manage cloud infrastructure using Terraform and infrastructure as code.", "category": "DevOps", "difficulty": "Intermediate", "price": 74.99, "instructor": "IaC Expert", "duration": "6 weeks", "tags": "devops,terraform,IaC,infrastructure"},
    {"title": "Monitoring and Observability", "description": "Set up comprehensive monitoring using Prometheus, Grafana, and ELK stack.", "category": "DevOps", "difficulty": "Intermediate", "price": 69.99, "instructor": "Monitoring Pro", "duration": "5 weeks", "tags": "devops,monitoring,prometheus,grafana"},
    
    # Web Development
    {"title": "Full Stack Web Development", "description": "Build complete web applications with React, Node.js, and databases.", "category": "Web Development", "difficulty": "Beginner", "price": 49.99, "instructor": "Web Dev Team", "duration": "12 weeks", "tags": "web,full-stack,react,nodejs"},
    {"title": "React.js Advanced Patterns", "description": "Master advanced React patterns, hooks, and performance optimization.", "category": "Web Development", "difficulty": "Advanced", "price": 79.99, "instructor": "React Expert", "duration": "6 weeks", "tags": "web,react,advanced,hooks"},
    {"title": "Next.js Production Apps", "description": "Build production-ready applications with Next.js, SSR, and edge functions.", "category": "Web Development", "difficulty": "Intermediate", "price": 74.99, "instructor": "Next.js Pro", "duration": "6 weeks", "tags": "web,nextjs,SSR,production"},
    {"title": "Web Security Essentials", "description": "Protect web applications from common vulnerabilities and security threats.", "category": "Web Development", "difficulty": "Intermediate", "price": 64.99, "instructor": "Security Expert", "duration": "4 weeks", "tags": "web,security,vulnerabilities,protection"},
]

def seed_products():
    """Add all 50 courses to database and ChromaDB"""
    print("Initializing database...")
    init_db()
    
    print("Initializing ChromaDB...")
    init_chroma()
    
    db = SessionLocal()
    
    # Clear existing products (optional)
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"Found {existing_count} existing products. Skipping duplicates...")
    
    added_count = 0
    
    for course in courses:
        # Check if product already exists
        existing = db.query(Product).filter(Product.title == course["title"]).first()
        if existing:
            print(f"⏭️  Skipping: {course['title']}")
            continue
        
        # Create product in SQLite
        product = Product(**course)
        db.add(product)
        db.flush()  # Get the ID
        
        # Create embedding and add to ChromaDB
        text_for_embedding = f"{course['title']} {course['description']} {course['category']} {course['tags']}"
        embedding = generate_simple_embedding(text_for_embedding)
        
        add_product_embedding(
            product_id=str(product.id),
            text=text_for_embedding,
            embedding=embedding,
            metadata={
                "title": course["title"],
                "category": course["category"],
                "difficulty": course["difficulty"],
                "product_id": product.id
            }
        )
        
        # Update chroma_id in product
        product.chroma_id = str(product.id)
        
        added_count += 1
        print(f"✅ Added: {course['title']} [{course['category']}]")
    
    db.commit()
    db.close()
    
    print(f"\n🎉 Successfully added {added_count} products!")
    print(f"📊 Total products in database: {db.query(Product).count() if hasattr(db, 'query') else added_count}")

if __name__ == "__main__":
    seed_products()