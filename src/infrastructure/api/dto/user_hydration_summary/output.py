from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
  id: str
  name: str
  email: EmailStr
  weightKg: float
  dailyGoalMl: float

class WaterIntakeResponse(BaseModel):
  id: str
  userId: str
  date: str
  ml: int
  isGoalAchieved: bool
  remainingMlToGoal: float
  goalAverage: float

class UserDayHydrationSummaryResponse(BaseModel):
  user: UserResponse
  waterIntake: Optional[WaterIntakeResponse]
