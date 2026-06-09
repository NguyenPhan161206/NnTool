#!/bin/sh
set -e

DEFAULT_MODEL=${OLLAMA_DEFAULT_MODEL:-qwen3:4b}

# Start ollama server in background
ollama serve &
OLLAMA_PID=$!

# Wait for server to be ready
echo "Waiting for ollama server..."
until ollama list 2>/dev/null; do
    sleep 1
done
echo "Ollama server ready."

# Pull default model if not present
if [ -n "$DEFAULT_MODEL" ]; then
    if ! ollama list 2>/dev/null | grep -q "^${DEFAULT_MODEL%%:*}"; then
        echo "Model $DEFAULT_MODEL not found. Pulling..."
        ollama pull "$DEFAULT_MODEL"
        echo "Model $DEFAULT_MODEL ready."
    else
        echo "Model $DEFAULT_MODEL already present."
    fi
fi

# Bring ollama serve to foreground
wait $OLLAMA_PID
