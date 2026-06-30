import httpx
import datetime
import sys

url = "http://127.0.0.1:8000"

def run_tests():
    with httpx.Client(timeout=120.0) as client:
        print("0. Testing GET /execution-plan (Initial State)")
        r = client.get(f"{url}/execution-plan")
        assert r.status_code == 200, f"GET /execution-plan failed: {r.text}"
        print("[PASS] Execution plan initial state works")

        print("0.1 Testing POST /projects")
        r = client.post(f"{url}/projects", json={"name": f"Regression Project {datetime.datetime.now().timestamp()}"})
        assert r.status_code == 200, f"POST /projects failed: {r.text}"
        project_id = r.json()["id"]
        print("[PASS] Project creation works")
        
        print("0.2 Testing GET /projects")
        r = client.get(f"{url}/projects")
        assert r.status_code == 200, "GET /projects failed"
        assert any(p["id"] == project_id for p in r.json()), "Project not found in list"
        print("[PASS] Project listing works")

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
        
        # Create a second task to test sorting
        r2 = client.post(f"{url}/tasks", json={
            "title": "Regression Test Task 2",
            "priority": "low"
        })
        assert r2.status_code == 200, "POST /tasks failed"
        
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
        
        print("4.1 Testing GET /projects/{id}")
        r = client.get(f"{url}/projects/{project_id}")
        assert r.status_code == 200, "GET /projects/{id} failed"
        data = r.json()
        assert "project" in data
        assert "progress" in data
        assert "responsibilities" in data
        print("[PASS] Project overview works")

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
        
        print("7. Testing POST /advisor")
        r = client.post(f"{url}/advisor", json={"question": "Can I game tonight?"})
        assert r.status_code == 200, "POST /advisor failed"
        print("[PASS] Advisor works")

        print("8. Testing GET /execution-plan (Populated State)")
        r = client.get(f"{url}/execution-plan")
        assert r.status_code == 200, f"GET /execution-plan failed: {r.text}"
        print("[PASS] Execution plan populated state works")

        print("\nALL TESTS PASSED! Sprint 7 regression testing successful.")

if __name__ == "__main__":
    run_tests()
