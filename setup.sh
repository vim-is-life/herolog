#!/usr/bin/env sh
set -e

# create the virtual environment
python3 -m venv .venv

if [ $INSTALL_DEPS ]; then
    . .venv/bin/activate
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip3 install django
fi
