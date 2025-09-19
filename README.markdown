# Video Generation Service

This project is a FastAPI-based application that generates promotional videos with animated text overlays using OpenCV and PIL. It supports downloading images from Google Drive URLs, rendering text with custom animations (e.g., top-to-down for rural audiences, right-to-left for urban audiences), and exporting the result as an MP4 file.

## Features
- Download images from Google Drive URLs.
- Generate videos with animated text overlays.
- Support for rural and urban audience-specific animations.
- Text wrapping and adjustable font size for better fit.
- 5-second duration per text line with fade-in effects.

## Prerequisites
- Python 3.8 or higher
- Required dependencies (see `requirements.txt`)

## Installation


1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the `app/assets/fonts/Nirmala.ttf` font file is available in the project directory.

## Usage

### Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Replace `app.main` with the path to your main FastAPI file (e.g., `app/main.py` if your entry point is there).

### API Endpoints
- **POST `/generate_video`**: Generate a video with text overlays.
  - **Request Body**: JSON object with `image_url` (Google Drive URL), `text` (string with `\n` for new lines), and `audience` (e.g., "rural" or "urban").
    ```json
    {
      "image_url": "https://drive.google.com/file/d/123456789/view",
      "text": "Chhupana kyun, jab protect karna easy hai?\nApni health ke liye India ka smart choice – MAI sanitary pads.\nHar din safe, har din comfortable.",
      "audience": "urban"
    }
    ```
  - **Response**: JSON with the path to the generated video file.
    ```json
    {
      "video_path": "outputs/image_hash_urban.mp4"
    }
    ```

### Example Request
Using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/generate_video" \
-H "Content-Type: application/json" \
-d '{"image_url": "https://drive.google.com/file/d/123456789/view", "text": "Chhupana kyun, jab protect karna easy hai?\nApni health ke liye India ka smart choice – MAI sanitary pads.\nHar din safe, har din comfortable.", "audience": "urban"}'
```

## Configuration
- Output directory: `outputs` (configurable via `output_dir` parameter).
- Video resolution: 720x720 (adjustable via `width` and `height` parameters).
- FPS: 25 (adjustable via `fps` parameter).

## Dependencies
All dependencies are listed in `requirements.txt`. Ensure you install them using:
```bash
pip install -r requirements.txt
```

## Development
- Use the `--reload` flag with `uvicorn` for automatic reloading during development.
- Modify `VideoService` in `app/services/video_service.py` to adjust animations or add new features.

## License
[Add your license here, e.g., MIT, Apache 2.0, or specify if none]

## Contributing
Feel free to submit issues or pull requests. Please follow the existing code style and include tests if applicable.