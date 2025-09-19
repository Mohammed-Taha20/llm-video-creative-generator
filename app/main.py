from fastapi import FastAPI
from app.routes import video_routes

app = FastAPI(title="Creative Generator API")
app.include_router(video_routes.router, prefix="/api", tags=["creatives"])
