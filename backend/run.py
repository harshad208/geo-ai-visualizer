import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "True").lower() == "true"

    print(f"Starting server on http://{host}:{port}")
    if reload:
        print("Auto-reloading is enabled.")

    uvicorn.run(
        "app.main:app",  
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )