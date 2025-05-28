from domain.shared.exceptions import DomainBadRequestError

from domain.user.constants import DAILY_WATER_ML_PER_KG

from domain.user.value_objects import Email

class User:
  def __init__(self, id: str, name: str, email: Email, weight_kg: float, daily_goal_ml: int = None ):
    if not name.strip():
      raise DomainBadRequestError('Name cannot be empty.')
    
    if weight_kg <= 0:
      raise DomainBadRequestError('Weight must be greater than zero.')

    self.id = id
    self.name = name
    self.email = email
    self.weight_kg = weight_kg
    self.daily_goal_ml = daily_goal_ml if daily_goal_ml is not None else int(weight_kg * DAILY_WATER_ML_PER_KG)

  def __str__(self) -> str:
    return (
      f'User(name={self.name}, email={self.email}, '
      f'weight_kg={self.weight_kg}kg, daily_goal_ml={self.daily_goal_ml}ml)'
    )

  def __repr__(self) -> str:
    return (
      f'User('
      f'id={self.id!r}, '
      f'name={self.name!r}, '
      f'email={self.email!r}, '
      f'weight_kg={self.weight_kg}, '
      f'daily_goal_ml={self.daily_goal_ml}'
      f')'
    )