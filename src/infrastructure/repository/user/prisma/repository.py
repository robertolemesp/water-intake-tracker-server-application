import logging

from domain.user.repository import UserRepository

from infrastructure.database.connection import DatabaseConnection

logger = logging.getLogger("uvicorn.error")

class PrismaUserRepository(UserRepository):
  def __init__(self, db: DatabaseConnection):
    self.db = db

  async def get_by_email(self, user_email: str) -> dict:
    try:
      user = await self.db.user.find_unique(where={'email': user_email})

      if not user:
        return None

      return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'weight_kg': user.weightKg,
        'daily_goal_ml': user.dailyGoalMl
      }
    except Exception as e:
      logger.exception('PrismaUserRepository.get_by_email error occurred')
      raise e

  async def save(self, data: dict) -> dict:
    try:
      await self.db.user.create(
        data={
          'name': data['name'],
          'email': data['email'],
          'weightKg': data['weight_kg'],
          'dailyGoalMl': data['daily_goal_ml']
        }
      )

      created_user = await self.db.user.find_unique(
        where={'email': data['email']}
      )

      return {
        'id': created_user.id,
        'name': created_user.name,
        'email': created_user.email,
        'weight_kg': created_user.weightKg,
        'daily_goal_ml': created_user.dailyGoalMl
      }
    except Exception as e:
      logger.exception('PrismaUserRepository.save error occurred')
      raise e