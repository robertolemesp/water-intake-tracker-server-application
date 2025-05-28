from infrastructure.api.router.routes.user import router as user_router
from infrastructure.api.router.routes.water_intake import router as water_intake_router
from infrastructure.api.router.routes.user_hydration_summary import router as hydration_summary_router

__all__ = [
  'user_router',
  'water_intake_router',
  'hydration_summary_router'
]
