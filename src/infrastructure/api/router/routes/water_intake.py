from fastapi import APIRouter, Depends
from typing import List

from infrastructure.api.dto.water_intake.register import WaterIntakeResponse, RegisterWaterIntakeRequest
from infrastructure.api.controllers.water_intake import WaterIntakeController

from infrastructure.dependency_injection import di_container


router = APIRouter(prefix='/water-intake', tags=['Water Intake'])

@router.post('/{user_id}/register', response_model=WaterIntakeResponse, summary='Register water intake')
async def register_water_intake(
  user_id: str,
  payload: RegisterWaterIntakeRequest,
  controller: WaterIntakeController = Depends(lambda: di_container.water_intake_controller)
):
  return await controller.register(user_id, payload)


@router.get('/{user_id}/history', response_model=List[WaterIntakeResponse], summary='Retrieve water intake history')
async def get_water_intake_history(
  user_id: str,
  controller: WaterIntakeController = Depends(lambda: di_container.water_intake_controller)
):
  return await controller.retrieve_history(user_id)
