from dataclasses import asdict
from typing import List

from infrastructure.api.dto.water_intake.register import RegisterWaterIntakeRequest, WaterIntakeResponse 

from application.water_intake.services.register_intake import RegisterWaterIntakeUseCase
from application.water_intake.services.retrieve_history import RetrieveWaterIntakeHistoryUseCase

class WaterIntakeController:
  def __init__(self, di_container):
    self.register_use_case: RegisterWaterIntakeUseCase = di_container.register_water_intake_use_case
    self.retrieve_history_use_case: RetrieveWaterIntakeHistoryUseCase = di_container.retrieve_water_intake_history_use_case

  async def register(self, user_id: str, payload: RegisterWaterIntakeRequest) -> WaterIntakeResponse:
    output = await self.register_use_case.execute(user_id, payload)
    return WaterIntakeResponse.model_validate(asdict(output))

  async def retrieve_history(self, user_id: str) -> List[WaterIntakeResponse]:
    output = await self.retrieve_history_use_case.execute(user_id)
    return [WaterIntakeResponse.model_validate(asdict(item)) for item in output]
