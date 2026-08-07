from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text('ALTER TABLE user_behaviors ADD COLUMN time_spent FLOAT'))
        conn.commit()
        print('✅ time_spent column added')
    except Exception as e:
        print('Column may already exist:', e)