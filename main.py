import logging
import random
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Capybara Image Fetcher")


def get_codes_from_fastapi():
    """Get HTTP status codes from FastAPI"""
    try:
        # Get all HTTP status constants from FastAPI
        codes = []
        for attr_name in dir(status):
            if attr_name.startswith("HTTP_"):
                code = getattr(status, attr_name)
                if isinstance(code, int):
                    codes.append(code)
        return sorted(codes)
    except ImportError:
        return []


IMAGES_DIR = Path.home() / "images"
IMAGES_DIR.mkdir(exist_ok=True)

@app.get("/")
async def get_capybara():
    random_code = random.choice(get_codes_from_fastapi())

    filename = f"capybara_{random_code}.jpg"
    filepath = IMAGES_DIR / filename

    # Check if file already exists
    if filepath.exists():
        logger.info(f"Using cached image: {filepath}")
        return Response(content=filepath.read_bytes(), media_type="image/jpeg")

    url = f"https://capy.codes/{random_code}.jpg"
    logger.info(f"Fetching capybara image from: {url}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                logger.info(f"Image saved and serving: {filepath}")

                return Response(content=response.content, media_type="image/jpeg")
            else:
                logger.warning(
                    f"Failed to fetch image for code {random_code}. Status: {response.status_code}"
                )
                raise HTTPException(
                    status_code=404,
                    detail=f"No capybara image found for code {random_code}",
                )

    except httpx.RequestError as e:
        logger.error(f"Request error when fetching {url}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch capybara image due to network error",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
