import sys
from app.awareness.models import Insight, InsightSeverity

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("Creating valid insight...")
    try:
        insight = Insight(
            title="Overloaded Tomorrow",
            description="Tomorrow contains more planned work than available capacity.",
            severity=InsightSeverity.HIGH
        )
        print("✓ Success")
    except Exception as e:
        print(f"✗ Failed: {e}")
        
    print("\nCreating invalid insight (empty title)...")
    try:
        insight = Insight(
            title="",
            description="Tomorrow contains more planned work than available capacity.",
            severity=InsightSeverity.HIGH
        )
        print("✗ Success")
    except ValueError:
        print("✓ Expected ValueError")
        
    print("\nCreating invalid insight (empty description)...")
    try:
        insight = Insight(
            title="Overloaded Tomorrow",
            description="   ",
            severity=InsightSeverity.HIGH
        )
        print("✗ Success")
    except ValueError:
        print("✓ Expected ValueError")

if __name__ == "__main__":
    main()
