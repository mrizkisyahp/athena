import httpx
import datetime

url = 'http://127.0.0.1:8000'

# We use UTC times here so it cleanly aligns with the server's utcnow() usage.
now = datetime.datetime.utcnow()
today = now.isoformat() + 'Z'
yesterday = (now - datetime.timedelta(days=1)).isoformat() + 'Z'

print("Creating 'Employee report' (Due today)...")
httpx.post(f'{url}/tasks', json={'title': 'Employee report', 'due_date': today})

print("Creating 'Thesis' (Due yesterday)...")
httpx.post(f'{url}/tasks', json={'title': 'Thesis', 'due_date': yesterday})

print("Creating 'Grocery shopping' (Due today, completed)...")
r3 = httpx.post(f'{url}/tasks', json={'title': 'Grocery shopping', 'due_date': today}).json()

print(f"Completing 'Grocery shopping' (ID: {r3['id']})...")
httpx.patch(f'{url}/tasks/{r3["id"]}/complete')

print("\nTasks have been populated! You can now check GET /today in Swagger.")
