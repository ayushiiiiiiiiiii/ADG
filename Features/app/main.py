from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Features Extraction API",
    description="A service that parses Python and Java code and extracts code features.",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
