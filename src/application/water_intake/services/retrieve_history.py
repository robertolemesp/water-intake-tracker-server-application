import logging
    
from application.water_intake.dto.output import WaterIntakeOutput
from domain.water_intake.entity import WaterIntake
from domain.water_intake.repository import WaterIntakeRepository

logger = logging.getLogger("uvicorn.error")

class RetrieveWaterIntakeHistoryUseCase:
  def __init__(self, water_intake_repo: WaterIntakeRepository):
    self.water_intake_repo = water_intake_repo

  async def execute(self, user_id: str) -> list[WaterIntakeOutput]:
    try:
      found_water_intakes = await self.water_intake_repo.get_all_by_user_id(user_id)

      water_intakes = [
        WaterIntake(
          id=found_water_intake['id'],
          user_id=found_water_intake['user_id'],
          date=found_water_intake['date'],
          ml=found_water_intake['ml'],
          is_goal_achieved=found_water_intake['is_goal_achieved'],
          remaining_ml_to_goal=found_water_intake['remaining_ml_to_goal'],
          goal_average=found_water_intake['goal_average']
        )
        for found_water_intake in found_water_intakes
      ]

      return [
        WaterIntakeOutput(
          id=water_intake.id,
          userId=user_id,
          date=water_intake.date.isoformat(),
          ml=water_intake.ml,
          isGoalAchieved=water_intake.is_goal_achieved,
          remainingMlToGoal=water_intake.remaining_ml_to_goal,
          goalAverage=water_intake.goal_average
        )
        for water_intake in water_intakes
      ]
    
    except Exception as e:
      logger.exception('RetrieveWaterIntakeHistoryUseCase.execute error occurred')
      raise e