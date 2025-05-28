from fastapi import APIRouter, Depends

from infrastructure.api.dto.user_hydration_summary.output import UserDayHydrationSummaryResponse
from infrastructure.api.controllers.user_hydration_summary import UserHydrationSummaryController

from infrastructure.dependency_injection import di_container

router = APIRouter(prefix='/user-hydration-summary', tags=['Hydration Summary'])

@router.get('/{user_email}', response_model=UserDayHydrationSummaryResponse, summary='Retrieve hydration summary')
async def get_user_day_hydration_summary(
  user_email: str,
  controller: UserHydrationSummaryController = Depends(lambda: di_container.hydration_summary_controller)
):
  return await controller.get_user_day_hydration_summary(user_email)
