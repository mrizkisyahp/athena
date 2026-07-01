from app.workload.models import WorkloadAnalysis
from app.time.duration import Duration

def main():
    analysis = WorkloadAnalysis(
        total_workload=Duration(480),
        available_capacity=Duration(360),
        overloaded=True,
    )

    print(analysis)

if __name__ == "__main__":
    main()