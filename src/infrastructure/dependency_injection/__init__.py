from application.user.services.create import CreateUserUseCase
from application.water_intake.services.register_intake import RegisterWaterIntakeUseCase
from application.water_intake.services.retrieve_history import RetrieveWaterIntakeHistoryUseCase
from application.user_hydration_summary.services.retrieve_day_summary import RetrieveUserDayHydrationSummaryUseCase

from infrastructure.repository.user import UserRepository
from infrastructure.repository.water_intake import WaterIntakeRepository

from infrastructure.api.controllers.user import UserController
from infrastructure.api.controllers.water_intake import WaterIntakeController
from infrastructure.api.controllers.user_hydration_summary import UserHydrationSummaryController

from infrastructure.database.connection import DatabaseConnection


class DependencyInjectionContainer:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
        cls._instance = super(DependencyInjectionContainer, cls).__new__(cls)
    return cls._instance
  
  def __init__(self):
    self._db = None

    self._user_repository = None
    self._water_intake_repository = None

    self._user_create_use_case = None
    self._register_water_intake_use_case = None
    self._retrieve_water_intake_history_use_case = None
    self._retrieve_day_hydration_summary_use_case = None

    self._user_controller = None
    self._water_intake_controller = None
    self._hydration_summary_controller = None

  async def init(self):
    self._db = DatabaseConnection.get_client()
    await self._db.connect()

    self._user_repository = UserRepository(self._db)
    self._water_intake_repository = WaterIntakeRepository(self._db)

    self._user_create_use_case = CreateUserUseCase(self._user_repository)
    self._register_water_intake_use_case = RegisterWaterIntakeUseCase(self._water_intake_repository)
    self._retrieve_water_intake_history_use_case = RetrieveWaterIntakeHistoryUseCase(self._water_intake_repository)
    self._retrieve_user_day_hydration_summary_use_case = RetrieveUserDayHydrationSummaryUseCase(self._user_repository, self._water_intake_repository)

    self._user_controller = UserController(self)
    self._water_intake_controller = WaterIntakeController(self)
    self._hydration_summary_controller = UserHydrationSummaryController(self)

  async def shutdown(self):
    await self._db.disconnect()


  @property
  def user_repository(self) -> UserRepository:
    return self._user_repository

  @property
  def water_intake_repository(self) -> WaterIntakeRepository:
    return self._water_intake_repository


  @property
  def user_create_use_case(self) -> CreateUserUseCase:
    return self._user_create_use_case

  @property
  def register_water_intake_use_case(self) -> RegisterWaterIntakeUseCase:
    return self._register_water_intake_use_case

  @property
  def retrieve_water_intake_history_use_case(self) -> RetrieveWaterIntakeHistoryUseCase:
    return self._retrieve_water_intake_history_use_case

  @property
  def retrieve_user_day_hydration_summary_use_case(self) -> RetrieveUserDayHydrationSummaryUseCase:
    return self._retrieve_user_day_hydration_summary_use_case


  @property
  def user_controller(self) -> UserController:
    return self._user_controller

  @property
  def water_intake_controller(self) -> WaterIntakeController:
    return self._water_intake_controller

  @property
  def hydration_summary_controller(self) -> UserHydrationSummaryController:
    return self._hydration_summary_controller


di_container = DependencyInjectionContainer()
