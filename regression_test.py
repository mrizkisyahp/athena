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
            "due_date": now,
            "estimated_duration_minutes": 120
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
        created_task = next(t for t in tasks if t["id"] == task_id)
        assert created_task["estimated_duration_minutes"] == 120, "Estimated duration missing"
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

        print("9. Testing POST /advisor/capacity")
        r = client.post(f"{url}/advisor/capacity", json={"question": "I have 5 hours today."})
        assert r.status_code == 200, f"POST /advisor/capacity failed: {r.text}"
        print("[PASS] Capacity advisor works")

        print("10. Testing POST /workload (Scenario 1 & 2)")
        tasks = client.get(f"{url}/tasks").json()
        for t in tasks:
            if t["status"] != "completed":
                client.patch(f"{url}/tasks/{t['id']}/complete")
        
        p1 = client.post(f"{url}/projects", json={"name": "Workload Proj A"}).json()
        p2 = client.post(f"{url}/projects", json={"name": "Workload Proj B"}).json()
        
        t1 = client.post(f"{url}/tasks", json={"title": "T1", "priority": "high", "estimated_duration_minutes": 120, "project_id": p1["id"]}).json()
        t2 = client.post(f"{url}/tasks", json={"title": "T2", "priority": "high", "estimated_duration_minutes": 60, "project_id": p1["id"]}).json()
        t3 = client.post(f"{url}/tasks", json={"title": "T3", "priority": "high", "estimated_duration_minutes": 120, "project_id": p2["id"]}).json()
        
        r1 = client.post(f"{url}/workload", json={"available_minutes": 360}, timeout=60.0)
        assert r1.status_code == 200, f"Scenario 1 failed: {r1.text}"
        print("[PASS] Workload Scenario 1 works")
        
        r2 = client.post(f"{url}/workload", json={"available_minutes": 240}, timeout=60.0)
        assert r2.status_code == 200, f"Scenario 2 failed: {r2.text}"
        print("[PASS] Workload Scenario 2 works")
        
        print("11. Testing POST /workload (Scenario 3)")
        client.patch(f"{url}/tasks/{t1['id']}/complete")
        client.patch(f"{url}/tasks/{t2['id']}/complete")
        client.patch(f"{url}/tasks/{t3['id']}/complete")
        
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat() + "Z"
        today = datetime.datetime.now().isoformat() + "Z"
        
        client.post(f"{url}/tasks", json={"title": "Overdue Task", "priority": "high", "due_date": yesterday, "estimated_duration_minutes": 60})
        client.post(f"{url}/tasks", json={"title": "Critical Task", "priority": "critical", "due_date": today, "estimated_duration_minutes": 60})
        
        r3 = client.post(f"{url}/workload", json={"available_minutes": 60}, timeout=60.0)
        assert r3.status_code == 200, f"Scenario 3 failed: {r3.text}"
        print("[PASS] Workload Scenario 3 works")
        
        print("12. Testing POST /workload (Scenario 4)")
        r4 = client.post(f"{url}/workload", json={"available_minutes": 0})
        assert r4.status_code == 422, f"Scenario 4 failed: {r4.text}"
        print("[PASS] Workload Scenario 4 works")

        print("\nALL TESTS PASSED!\nSprint 9 regression testing successful.")

if __name__ == "__main__":
    run_tests()
