from app.utils.mesh_api import generate_recommendation_message
import asyncio

async def test():
    result = await generate_recommendation_message(
        'Python, AI, Machine Learning',
        [
            {'title': 'Python Basics', 'category': 'Python', 'difficulty': 'Beginner', 'description': 'Learn Python from scratch'}
        ]
    )
    print('Result:', result)

asyncio.run(test())