from datetime import date, datetime
import logging

from domain.shared.exceptions import DomainBadRequestError, DomainNotFoundError
from domain.water_intake.repository import WaterIntakeRepository
from domain.water_intake.entity import WaterIntake

from application.water_intake.dto.input import WaterIntakeInput
from application.water_intake.dto.output import WaterIntakeOutput

logger = logging.getLogger("uvicorn.error")

class RegisterWaterIntakeUseCase:
  def __init__(self, repo: WaterIntakeRepository):
    self.repo = repo

  async def execute(self, user_id: str, water_intake_input: WaterIntakeInput) -> WaterIntakeOutput:
    try:
      existing_day_water_intake = await self.repo.get_by_user_and_date(user_id, date.today(), water_intake_input.ml)

      if existing_day_water_intake:
        water_intake = WaterIntake(
          id=existing_day_water_intake['id'],
          user_id=existing_day_water_intake['user_id'],
          date=datetime.fromisoformat(existing_day_water_intake['date']).date(),
          ml=existing_day_water_intake['ml'],
          is_goal_achieved=existing_day_water_intake['is_goal_achieved'],
          remaining_ml_to_goal=existing_day_water_intake['remaining_ml_to_goal'],
          goal_average=existing_day_water_intake['goal_average']
        )
        water_intake.add(water_intake_input.ml)
      elif not water_intake_input.userDailyGoalMl:
        raise DomainBadRequestError('First water intake register must have the daily goal ml.')
      else:
        water_intake = WaterIntake(
          id='',
          user_id=user_id,
          ml=water_intake_input.ml
        )

        water_intake.calculate_progress(water_intake_input.userDailyGoalMl)

      await self.repo.save({
        'id': water_intake.id,
        'user_id': water_intake.user_id,
        'date': water_intake.date,
        'ml': water_intake.ml
      })

      return WaterIntakeOutput(
        id=water_intake.id,
        userId=water_intake.user_id,
        date=water_intake.date.isoformat(),
        ml=water_intake.ml,
        isGoalAchieved=water_intake.is_goal_achieved,
        remainingMlToGoal=water_intake.remaining_ml_to_goal,
        goalAverage=water_intake.goal_average
      )
    
    except Exception as e:
      logger.exception('RegisterWaterIntakeUseCase.execute error occurred')
      raise e
