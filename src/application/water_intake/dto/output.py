from dataclasses import dataclass

@dataclass
class WaterIntakeOutput:
  id: str
  userId: str
  date: str
  ml: int
  isGoalAchieved: bool
  remainingMlToGoal: float
  goalAverage: float
