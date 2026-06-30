import httpx
import datetime
import sys

url = "http://127.0.0.1:8000"

def run_tests():
    with httpx.Client(timeout=120.0) as client:
        print("1. Testing POST /chat")
        r = client.post(f"{url}/chat", json={"messages": [{"role": "user", "content": "Hello Athena!"}]})
        assert r.status_code == 200, "POST /chat failed"
        print("[PASS] Chat works")

        print("2. Testing POST /tasks")
        now = datetime.datetime.now().isoformat() + "Z"
        r = client.post(f"{url}/tasks", json={
            "title": "Regression Test Task",
            "priority": "critical",
            "due_date": now
        })
        assert r.status_code == 200, "POST /tasks failed"
        task_id = r.json()["id"]
        print("[PASS] Task creation works")

        print("3. Testing GET /tasks")
        r = client.get(f"{url}/tasks")
        assert r.status_code == 200, "GET /tasks failed"
        tasks = r.json()
        assert any(t["id"] == task_id for t in tasks), "Newly created task not found in GET /tasks"
        print("[PASS] List tasks works")

        print("4. Testing PATCH /tasks/{id}/complete")
        r = client.patch(f"{url}/tasks/{task_id}/complete")
        assert r.status_code == 200, "PATCH /complete failed"
        
        # Verify it completed
        r = client.get(f"{url}/tasks")
        completed_task = next(t for t in r.json() if t["id"] == task_id)
        assert completed_task["status"] == "completed", "Task status did not change to completed"
        assert completed_task["completed_at"] is not None, "completed_at was not populated"
        print("[PASS] Complete task works")

        print("5. Testing GET /today")
        r = client.get(f"{url}/today")
        assert r.status_code == 200, "GET /today failed"
        today_data = r.json()
        assert any(t["id"] == task_id for t in today_data["completed_today"]), "Task not in completed_today"
        print("[PASS] Today works")

        print("6. Testing GET /daily-briefing")
        r = client.get(f"{url}/daily-briefing")
        assert r.status_code == 200, "GET /daily-briefing failed"
        print("[PASS] Daily Briefing works")

        print("\nALL TESTS PASSED! PostgreSQL regression testing successful.")

if __name__ == "__main__":
    run_tests()
