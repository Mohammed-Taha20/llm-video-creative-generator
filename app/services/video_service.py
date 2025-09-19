import os
import re
import requests
from hashlib import md5
from app.models.request_model import CreativeRequest

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class VideoService:
    @classmethod
    def get_direct_drive_url(cls, url: str) -> str:
        """Convert Google Drive share link to direct download link"""
        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
        if not match:
            raise ValueError("Invalid Google Drive URL")
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    @classmethod
    def download_image(cls, url: str, output_dir="downloads") -> str:
        """Download image from Google Drive URL"""
        os.makedirs(output_dir, exist_ok=True)
        direct_url = cls.get_direct_drive_url(url)
        response = requests.get(direct_url, stream=True)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to download image: {response.status_code}")

        file_hash = md5(url.encode()).hexdigest()
        image_path = os.path.join(output_dir, f"{file_hash}.jpg")
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path

    @classmethod
    def generate_video_service(
        cls,
        request: CreativeRequest,
        output_dir="outputs",
        width=720,
        height=720,
        fps=25,
    ):
        """Generate a promotional video with animated text layers (cv2 + PIL)."""
        image_url, text, audience = request.image_url, request.text, request.audience
        os.makedirs(output_dir, exist_ok=True)

        # Step 1: download the image
        image_path = cls.download_image(image_url, output_dir)

        # Step 2: split text at newlines
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        per_line_duration = 5  # Each line displays for 5 seconds
        duration = len(lines) * per_line_duration  # Total video duration

        # Step 3: prepare video writer
        img = cv2.imread(image_path)
        if img is None:
            raise RuntimeError("Could not load image")
        img = cv2.resize(img, (width, height))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        base = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{base}_{audience}.mp4")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        font_path = os.path.join("app", "assets", "fonts", "Nirmala.ttf")
        if not os.path.exists(font_path):
            raise RuntimeError(f"Font not found: {font_path}")
        font_size = int(height * 0.05)  
        font = ImageFont.truetype(font_path, font_size)

        # Step 5: create frames with animated text overlays
        total_frames = duration * fps
        for frame_idx in range(total_frames):
            sec = frame_idx / fps
            frame_img = img.copy()

            # Convert to PIL for text rendering
            pil_img = Image.fromarray(cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_img)

            for i, line in enumerate(lines):
                start = i * per_line_duration
                end = (i + 1) * per_line_duration
                if start <= sec < end:
                    progress = (sec - start) / per_line_duration

                    # Wrap text if it exceeds frame width
                    wrapped_lines = []
                    words = line.split()
                    current_line = ""
                    for word in words:
                        test_line = f"{current_line} {word}".strip()
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        text_w = bbox[2] - bbox[0]
                        if text_w <= width - 20:  # Leave 10px margin on each side
                            current_line = test_line
                        else:
                            if current_line:
                                wrapped_lines.append(current_line)
                            current_line = word
                    if current_line:
                        wrapped_lines.append(current_line)

                    for j, wrapped_line in enumerate(wrapped_lines):
                        # Get text bounding box
                        bbox = draw.textbbox((0, 0), wrapped_line, font=font)
                        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                        y_offset = j * text_h
                        y_base = (height - (len(wrapped_lines) * text_h)) // 2

                        if audience.lower() == "rural":
                            start_y = -text_h  # Start off-screen
                            end_y = y_base + y_offset  # Target y for this wrapped line
                            anim_duration = 1.0  # Animation completes in 1 second
                            y = int(start_y + (end_y - start_y) * min(progress * (per_line_duration / anim_duration), 1))
                            x = (width - text_w) // 2
                        elif audience.lower() == "urban":
                            start_x = width  # Start off-screen to the right
                            end_x = (width - text_w) // 2  # Center
                            anim_duration = 1.0  # Animation completes in 1 second
                            x = int(start_x + (end_x - start_x) * min(progress * (per_line_duration / anim_duration), 1))
                            y = y_base + y_offset
                        else:
                            x = (width - text_w) // 2
                            y = y_base + y_offset

                        # Fade-in effect (over first 1 second)
                        alpha = int(255 * min(progress * (per_line_duration / 1.0), 1))  # Fade from 0 to 255
                        fill_color = (255, 255, 0, alpha)  # Yellow with alpha

                        # Draw text with shadow for better readability
                        draw.text((x + 2, y + 2), wrapped_line, font=font, fill=(0, 0, 0, alpha))  # Shadow
                        draw.text((x, y), wrapped_line, font=font, fill=fill_color)  # Main text

            # Convert back to cv2
            frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)

        out.release()
        return output_path