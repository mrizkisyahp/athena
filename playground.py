from app.responsibilities.models import Responsibility
from app.responsibilities.service import ResponsibilityService
from app.services.time_service import TimeService

def main():
    service = ResponsibilityService()
    
    # Run 1: Add and print
    # service.add(Responsibility(title="Ship Athena Phase 2", due_date=TimeService.now()))
    
    # Run 2: Just print
    print(service.get_all())

if __name__ == "__main__":
    main()