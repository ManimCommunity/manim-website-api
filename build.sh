#!/bin/bash
set -e

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add $HOME/.local/bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Generate requirements.txt
uv export --format requirements-txt --no-hashes > requirements.txt

mkdir -p public/
cp requirements.txt public/requirements.txt
cp -r api/ public/
