import httpx
import datetime

def main():
    url = "http://127.0.0.1:8000"
    
    today = datetime.datetime.now().isoformat() + "Z"

    # Seed some data via API first
    print("Creating 'Ship Athena Phase 2' (CRITICAL, Due today)...")
    httpx.post(f"{url}/tasks", json={
        "title": "Ship Athena Phase 2",
        "priority": "critical",
        "due_date": today
    })
    
    print("Creating 'Buy milk' (LOW, Due today)...")
    httpx.post(f"{url}/tasks", json={
        "title": "Buy milk",
        "priority": "low",
        "due_date": today
    })

    print("\nRequesting daily briefing (this may take a few seconds)...")
    
    # Increase timeout since LLM calls can take a bit
    response = httpx.get(f"{url}/daily-briefing", timeout=120.0)
    
    if response.status_code == 200:
        data = response.json()
        briefing = data.get("briefing", "")
        print("\n=== DAILY BRIEFING ===")
        # Using encode/decode to avoid Windows console cp1252 emoji errors
        print(briefing.encode("utf-8", "replace").decode("utf-8", "replace"))
        print("======================")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()