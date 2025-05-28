from pydantic import BaseModel
from typing import Optional

class RegisterWaterIntakeRequest(BaseModel):
  userDailyGoalMl: Optional[int]  = None
  ml: int

class WaterIntakeResponse(BaseModel):
  id: str
  userId: str
  date: str
  ml: int
  isGoalAchieved: bool
  remainingMlToGoal: float
  goalAverage: float
