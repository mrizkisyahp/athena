from app.time.duration import Duration

def main():
    print(Duration(15))
    print(Duration(90))
    print(Duration(120))
    
    try:
        print(Duration(0))
    except ValueError as e:
        print(f"Expected error caught: {e}")

if __name__ == "__main__":
    main()