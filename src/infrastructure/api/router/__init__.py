from fastapi import APIRouter
from infrastructure.api.router.routes import user, water_intake, user_hydration_summary

router = APIRouter()

router.include_router(user.router)
router.include_router(water_intake.router)
router.include_router(user_hydration_summary.router)
