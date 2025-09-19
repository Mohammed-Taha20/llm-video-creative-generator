from pydantic import BaseModel ,Field
from typing import Optional 

class CreativeRequest(BaseModel):
    """the request model for creating advertiseing creative short video"""
    image_url : str = Field(..., description = "URL of our product image")
    text : str = Field(..., description = "text about the benfit of our product")
    audience : str = Field (..., description = "Audience of the video", choices = ["rural" , "urban"])
    duration: int = Field(15, description="Duration of the video in seconds (10-20)")