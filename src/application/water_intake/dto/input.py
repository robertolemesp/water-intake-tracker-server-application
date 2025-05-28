from dataclasses import dataclass
from typing import Optional

@dataclass
class WaterIntakeInput:
  user_id: str
  user_daily_goal_ml: Optional[int]
  ml: int
