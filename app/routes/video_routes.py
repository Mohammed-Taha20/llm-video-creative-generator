from fastapi import APIRouter
from app.controllers.video_controller import generate_video_controller
from app.models.request_model import CreativeRequest
from app.models.respones_model import CreativeResponse

router = APIRouter()

@router.post("/generate-video", response_model=CreativeResponse)
async def generate_video(request : CreativeRequest):
    """generate a creative video based on the request"""
    return await generate_video_controller(request)
