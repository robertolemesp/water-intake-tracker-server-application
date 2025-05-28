from dataclasses import asdict

from infrastructure.api.dto.user.create import CreateUserRequest, CreateUserResponse
from application.user.services.create import CreateUserUseCase

class UserController:
  def __init__(self, di_container):
    self.user_create_use_case: CreateUserUseCase = di_container.user_create_use_case

  async def create(self, payload: CreateUserRequest) -> CreateUserResponse:
    output = await self.user_create_use_case.execute(payload)
    return CreateUserResponse.model_validate(asdict(output))