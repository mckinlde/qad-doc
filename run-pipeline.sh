#!/bin/bash

# Exit immediately if a command fails
set -e

# Constants
VIDEO_URL="https://dn720407.ca.archive.org/0/items/rick-roll/Rick%20Roll.mp4"
VIDEO_FILE="RickRoll.mp4"
VENV_PATH=".venv"
PYTHON_SCRIPT="live-video-effects-pipeline.py"

if [ ! -f "$VIDEO_FILE" ]; then
  echo "📥 Downloading video..."
  curl -L -o "$VIDEO_FILE" "$VIDEO_URL"
else
  echo "✅ Video already exists. Skipping download."
fi

echo "🐍 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "🎬 Running video conversion script..."
python "$PYTHON_SCRIPT"

echo "✅ Done."
