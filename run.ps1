# Run both backend and frontend for Big Shot - For Windows PowerShell

Write-Host "Starting Big Shot Application..." -ForegroundColor Green

# Start the backend API in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; py api.py"

# Wait a moment for the API to start
Start-Sleep -Seconds 2

# Start the frontend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; py main.py"

Write-Host "Both services starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: Will open automatically" -ForegroundColor Cyan
