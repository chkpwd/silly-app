# Capybara Image Fetcher

A FastAPI application that fetches capybara images from [capy.codes](https://capy.codes/) based on HTTP status codes.

## Installation

### Docker

```bash
docker pull ghcr.io/chkpwd/silly-app:latest
docker run -p 8000:8000 ghcr.io/chkpwd/silly-app:latest
```

### Build

```bash
poetry install
```

## Usage

### Local

```bash
uvicorn main:app --reload
```

### Docker

Container runs on port 8000 by default.

### Endpoints

- `GET /` - Returns a random capybara image

Images are cached locally in `$HOME/images` directory to avoid repeated downloads.

## How it works

1. Generates random HTTP status code or uses provided code
2. Fetches image from `https://capy.codes/{code}.jpg`
3. Saves image to filesystem
4. Returns image directly to browser
