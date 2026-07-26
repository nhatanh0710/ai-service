from fastapi import FastAPI

from app.routes.predict_delay import router as predict_delay_router

from app.utils.model_loader import load_model


app = FastAPI(
    title="AI Project Management Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():

    load_model()


app.include_router(
    predict_delay_router
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