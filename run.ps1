Write-Host 'Starting Water Intake Server Application...'

$env:PYTHONPATH = '.\src'

poetry run uvicorn src.main:app_api --reload --host 0.0.0.0 --port 8000 --log-level debug

Write-Host "Server App's API is running at http://127.0.0.1:8000"
