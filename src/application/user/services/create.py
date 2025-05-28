import logging

from application.user.dto.input import CreateUserInput
from application.user.dto.output import CreateUserOutput

from domain.shared.exceptions import DomainConflictError
from domain.user.entity import User
from domain.user.repository import UserRepository

logger = logging.getLogger("uvicorn.error")

class CreateUserUseCase:
  def __init__(self, repo: UserRepository):
    self.repo = repo

  async def execute(self, user_input: CreateUserInput) -> CreateUserOutput:
    try:
      existing_user = await self.repo.get_by_email(user_input.email)
      if existing_user:
        raise DomainConflictError('User', 'email already exists')
      
      user = User(
        id='',
        name=user_input.name,
        email=user_input.email,
        weight_kg=user_input.weightKg
      )

      created_user = await self.repo.save({
        'id': user.id,
        'name': user.name,
        'email': str(user.email),
        'weight_kg': user.weight_kg,
        'daily_goal_ml': user.daily_goal_ml
      })

      return CreateUserOutput(
        id=created_user['id'],
        name=created_user['name'],
        email=created_user['email'],
        weightKg=created_user['weight_kg'],
        dailyGoalMl=created_user['daily_goal_ml']
      )
    
    except Exception as e:
      logger.exception('CreateUserUseCase.execute error occurred')
      raise e