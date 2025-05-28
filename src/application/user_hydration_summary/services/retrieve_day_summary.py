from datetime import date
import logging
    
from application.user_hydration_summary.dto.output import UserOutput, WaterIntakeOutput, UserDayHydrationSummaryOutput

from domain.shared.exceptions import DomainNotFoundError

from domain.user.entity import User
from domain.user.repository import UserRepository
from domain.water_intake.repository import WaterIntakeRepository
from domain.water_intake.entity import WaterIntake

logger = logging.getLogger("uvicorn.error")

class RetrieveUserDayHydrationSummaryUseCase:
  def __init__(self, user_repo: UserRepository, water_intake_repo: WaterIntakeRepository):
    self.user_repo = user_repo
    self.water_intake_repo = water_intake_repo

  async def execute(self, user_email: str) -> UserDayHydrationSummaryOutput:
    ADDED_ML = 0

    try:
      found_user = await self.user_repo.get_by_email(user_email)
    
      if not found_user:
        raise DomainNotFoundError('User', user_email)
      
      user = User(
        id=found_user['id'],
        name=found_user['name'],
        email=found_user['email'],
        weight_kg=found_user['weight_kg'],
        daily_goal_ml=found_user['daily_goal_ml']
      )

      user_output = UserOutput(
        id=user.id,
        name=user.name,
        email=user.email,
        weightKg=user.weight_kg,
        dailyGoalMl=user.daily_goal_ml
      )
      
      existing_water_intake = await self.water_intake_repo.get_by_user_and_date(user.id, date.today(), ADDED_ML)

      if existing_water_intake:
        water_intake = WaterIntake(
          id=existing_water_intake['id'],
          user_id=existing_water_intake['user_id'],
          date=existing_water_intake['date'],
          ml=existing_water_intake['ml'],
          remaining_ml_to_goal=existing_water_intake['remaining_ml_to_goal'],
          goal_average=existing_water_intake['goal_average']
        )

        water_intake_output = WaterIntakeOutput(
          id=water_intake.id,
          userId=water_intake.user_id,
          date=water_intake.date.isoformat(),
          ml=water_intake.ml,
          isGoalAchieved=water_intake.is_goal_achieved,
          remainingMlToGoal=water_intake.remaining_ml_to_goal,
          goalAverage=water_intake.goal_average
        )
      else:
        water_intake_output = None

      return UserDayHydrationSummaryOutput(
        user=user_output,
        waterIntake=water_intake_output
      )
     
    except Exception as e:
      logger.exception('RetrieveUserDayHydrationSummaryUseCase.execute error occurred')
      raise e