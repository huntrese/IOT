# Project Setup

Follow these steps to set up the project environment:

## 1. Install `uv`

First, install [`uv`](https://github.com/astral-sh/uv), a fast Python package manager:

```bash
pip install uv
```

## 2. Sync dependencies

Next, install all project dependencies as defined in `pyproject.toml` and `requirements.txt`:

```bash
uv sync
```