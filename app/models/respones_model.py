from pydantic import BaseModel ,Field
from typing import Optional , Dict

class CreativeResponse(BaseModel):
    """the model's response for creating advertiseing creative short video"""
    video_url : str = Field(..., description = "URL of the generated creative advertiseing video")
