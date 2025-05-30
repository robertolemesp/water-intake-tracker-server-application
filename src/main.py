from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.logging import AppLogger
from infrastructure.api.middlewares.error_handler import add_error_handlers
from infrastructure.api.router import router

from infrastructure.dependency_injection import di_container

AppLogger.setup()
AppLogger.info('Initializing application...')

app_api = FastAPI(
  title='Water Intake Tracker - API',
  description='Track daily and historical water intake and hydration goals',
  version='1.0.0'
)

add_error_handlers(app_api)

app_api.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app_api.include_router(router)

@app_api.on_event('startup')
async def startup():
  await di_container.init()

@app_api.on_event('shutdown')
async def shutdown():
  await di_container.shutdown()
