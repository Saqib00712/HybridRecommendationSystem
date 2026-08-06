from app.database import SessionLocal, init_db
from app.models.user import User
from app.utils.security import get_password_hash

init_db()
db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.username == 'admin').first()
if not admin:
    admin = User(
        email='admin@smartreco.ai',
        username='admin',
        hashed_password=get_password_hash('admin123'),
        full_name='Admin User',
        role='admin'
    )
    db.add(admin)
    print('✅ Admin user created: admin / admin123')
else:
    # Update password
    admin.hashed_password = get_password_hash('admin123')
    print('✅ Admin password reset: admin / admin123')

# Check if test user exists
user = db.query(User).filter(User.username == 'user').first()
if not user:
    user = User(
        email='user@smartreco.ai',
        username='user',
        hashed_password=get_password_hash('user123'),
        full_name='Test User',
        role='user'
    )
    db.add(user)
    print('✅ Test user created: user / user123')
else:
    user.hashed_password = get_password_hash('user123')
    print('✅ Test user password reset: user / user123')

db.commit()
db.close()
print('\n🎉 Ready! You can now login.')