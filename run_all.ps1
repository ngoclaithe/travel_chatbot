$root = $PSScriptRoot

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; rasa run actions"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; rasa run --enable-api --cors '*'"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; . .\.venv\Scripts\Activate.ps1; cd backend; python run.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\chatbot_fe`"; npm run dev"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "flutter emulators --launch Medium_Phone_API_36.1 --cold"

Start-Sleep -Seconds 60

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\chatbot_mb`"; flutter run -d android"
