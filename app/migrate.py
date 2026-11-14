import traceback
from app import initialize_database

if __name__ == "__main__":
    print("Starting StreamFlix database migration...", flush=True)
    try:
        initialize_database()
        print("SUCCESS: database schema is ready and catalogue is seeded.", flush=True)
    except Exception as exc:
        print(f"FAILED: database migration error: {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        raise
