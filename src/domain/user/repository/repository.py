from abc import ABC, abstractmethod

from domain.user.entity import User

class UserRepository(ABC):
  @abstractmethod
  async def save(self, user: User):
    ...

  @abstractmethod
  async def get_by_email(self, user_email: str) -> User:
    ...
