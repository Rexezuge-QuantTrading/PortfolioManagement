#!/bin/sh

uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir src
