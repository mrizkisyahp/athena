from app.projects.service import ProjectService

def main():
    service = ProjectService()
    
    service.create("Athena")
    service.create("Thesis")
    
    print("All projects:")
    for p in service.get_all():
        print(f"- {p.name} ({p.id})")
        
    print("\nTesting duplicate name...")
    try:
        service.create("Athena")
        print("FAIL: Expected ValueError")
    except ValueError as e:
        print(f"PASS: Caught expected error -> {e}")

if __name__ == "__main__":
    main()