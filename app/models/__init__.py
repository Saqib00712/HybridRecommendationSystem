# Models package
from app.models.user import User
from app.models.product import Product
from app.models.behavior import UserBehavior
from app.models.recommendation import Recommendation

__all__ = ["User", "Product", "UserBehavior", "Recommendation"]