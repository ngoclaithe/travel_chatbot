$root = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; rasa run actions"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; rasa run --enable-api --cors '*'"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; cd backend; python run.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\chatbot_fe`"; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\chatbot_mb`"; flutter run -d android"
