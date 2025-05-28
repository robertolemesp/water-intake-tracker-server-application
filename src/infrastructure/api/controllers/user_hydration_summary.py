from dataclasses import asdict

from application.user_hydration_summary.services.retrieve_day_summary import RetrieveUserDayHydrationSummaryUseCase
from application.user_hydration_summary.dto.output import UserDayHydrationSummaryOutput
from infrastructure.api.dto.user_hydration_summary.output import UserDayHydrationSummaryResponse

class UserHydrationSummaryController:
  def __init__(self, di_container):
    self.retrieve_user_day_hydration_summary: RetrieveUserDayHydrationSummaryUseCase = di_container.retrieve_user_day_hydration_summary_use_case

  async def get_user_day_hydration_summary(self, user_email: str) -> UserDayHydrationSummaryResponse:
    output = await self.retrieve_user_day_hydration_summary.execute(user_email)
    return UserDayHydrationSummaryResponse.model_validate(asdict(output))
