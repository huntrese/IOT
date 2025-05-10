# Project Setup

Follow these steps to set up the project environment:

## 1. Install `uv`

Install [`uv`](https://github.com/astral-sh/uv), a fast Python package manager:

```bash
pip install uv
```

## 2. Sync Dependencies

Install all project dependencies defined in `pyproject.toml` and `requirements.txt`:

```bash
uv sync
```

## 3. Running the RTSP Server

To run the RTSP server, use the following Docker command:

```bash
docker run --rm -p 8554:8554 aler9/rtsp-simple-server
```

This will start the server on port `8554`.