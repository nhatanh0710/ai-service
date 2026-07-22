from fastapi import FastAPI

app = FastAPI(
    title="AI Project Management Service",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "AI Service is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }