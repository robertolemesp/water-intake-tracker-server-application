from abc import ABC, abstractmethod
from datetime import date
from typing import List

from domain.water_intake.entity import WaterIntake

class WaterIntakeRepository(ABC):
  @abstractmethod
  async def get_by_user_and_date(self, user_id: str, date: date) -> dict | None:
    ...

  @abstractmethod
  async def save(self, water_intake: WaterIntake):
    ...

  @abstractmethod
  async def get_all_by_user_id(self, user_id: str) -> List[dict]:
    ...
