#!/usr/bin/env bash
set -e
uvicorn src.app:app --host 0.0.0.0 --port 8000
