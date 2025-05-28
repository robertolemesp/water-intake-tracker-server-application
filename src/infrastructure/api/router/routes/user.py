from fastapi import APIRouter, Depends

from infrastructure.api.dto.user.create import CreateUserRequest, CreateUserResponse
from infrastructure.api.controllers.user import UserController

from infrastructure.dependency_injection import di_container


router = APIRouter(prefix='/user', tags=['User'])

@router.post('/', response_model=CreateUserResponse, summary='Create a new user')
async def create_user(
  payload: CreateUserRequest,
  controller: UserController = Depends(lambda: di_container.user_controller)
):
  return await controller.create(payload)
