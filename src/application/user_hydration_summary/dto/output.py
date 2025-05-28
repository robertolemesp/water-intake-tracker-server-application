from dataclasses import dataclass
from typing import Optional

@dataclass
class UserOutput:
  id: str
  name: str
  email: str
  weightKg: float
  dailyGoalMl: float

@dataclass
class WaterIntakeOutput:
  id: str
  userId: str
  date: str
  ml: int
  isGoalAchieved: bool
  remainingMlToGoal: float
  goalAverage: float

@dataclass
class UserDayHydrationSummaryOutput:
  user: UserOutput
  waterIntake: Optional[WaterIntakeOutput]
