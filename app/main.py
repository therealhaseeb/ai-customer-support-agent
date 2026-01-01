from fastapi import FastAPI
from app.api.routes import router
from app.services.logger import logger

app = FastAPI(title="AI Customer Support Agent")

# Include API router
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Customer Support Agent is running"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
