from typing import Optional, Union
from datetime import date as dt_date, datetime

from domain.shared.exceptions import DomainBadRequestError

class WaterIntake:
  def __init__(
    self, 
    id: Optional[str], 
    user_id: str, 
    ml: int, 
    date: Optional[Union[dt_date, str]] = None, 
    is_goal_achieved: bool = False,
    remaining_ml_to_goal: float = 0.0, 
    goal_average: float = 0.0
  ):
    self.id = id
    self.user_id = user_id
    self.ml = ml
    self.date = self._parse_date(date) if date else dt_date.today()
    self.is_goal_achieved = is_goal_achieved
    self.remaining_ml_to_goal = remaining_ml_to_goal
    self.goal_average = goal_average


  @staticmethod
  def _parse_date(value: Union[dt_date, str]) -> dt_date:
    if isinstance(value, dt_date):
      return value
    if isinstance(value, str):
      try:
        return datetime.fromisoformat(value.rstrip('Z')).date()
      except ValueError:
        raise DomainBadRequestError(f'Invalid date format: {value}')
    raise DomainBadRequestError(f'Invalid date type: {type(value)}')


  def add(self, ml: int):
    if ml <= 0:
      raise DomainBadRequestError('Ingested amount must be positive.')
    self.ml += ml

  def calculate_progress(self, daily_goal_ml: float):
    if daily_goal_ml is None or daily_goal_ml <= 0:
       raise DomainBadRequestError('Daily goal Ml must be provided and positive.')
    
    ml = float(self.ml)

    remaining = max(daily_goal_ml - ml, 0.0)
    percentage = (ml / daily_goal_ml) * 100.0 if daily_goal_ml > 0 else 0.0
    is_goal_achieved = ml >= daily_goal_ml
    
    self.remaining_ml_to_goal = round(remaining, 2)
    self.goal_average = round(percentage, 2)
    self.is_goal_achieved = is_goal_achieved

  def __str__(self) -> str:
    return (
      f'WaterIntake(id={self.id}, user_id={self.user_id}, '
      f'ml={self.ml}, '
      f'date={self.date}, '
      f'is_goal_achieved={self.is_goal_achieved}, '
      f'remaining_ml_to_goal={self.remaining_ml_to_goal}ml, '
      f'goal_average={self.goal_average}%)'
    )

  def __repr__(self) -> str:
    return (
      f'WaterIntake('
      f'id={self.id!r}, '
      f'user_id={self.user_id!r}, '
      f'ml={self.ml}, '
      f'date={self.date!r}, '
      f'is_goal_achieved={self.is_goal_achieved}, '
      f'remaining_ml_to_goal={self.remaining_ml_to_goal}, '
      f'goal_average={self.goal_average}'
      f')'
    )