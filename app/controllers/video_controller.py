from app.services.video_service import VideoService
from app.models.request_model import CreativeRequest
from app.models.respones_model import CreativeResponse

async def generate_video_controller(request:CreativeRequest):
    """generate a creative video based on the request"""
    output_path = VideoService.generate_video_service(request)
    return CreativeResponse(video_url=output_path)
