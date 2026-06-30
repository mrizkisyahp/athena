from app.bootstrap.container import container
from app.time.duration import Duration

def main():
    service = container.responsibilities
    
    all_tasks = service.get_all()
    sprint_8 = next((t for t in all_tasks if t.title == "Sprint 8"), None)
    
    if not sprint_8:
        print("Creating Sprint 8 task...")
        sprint_8 = service.create(
            title="Sprint 8",
            estimated_duration=Duration(90)
        )
        print("Task created.")
    
    print(sprint_8.estimated_duration)

if __name__ == "__main__":
    main()